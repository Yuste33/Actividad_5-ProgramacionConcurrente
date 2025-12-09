import asyncio
import rx
from rx import operators as ops
from rx.subject import Subject
from rx.scheduler.eventloop import AsyncIOScheduler
from app.services.stream_factory import create_movement_stream, create_temp_stream, create_heart_stream
from app.models.schemas import Alert
from app.core.logger import logger


class JurassicProcessor:
    def __init__(self):
        self.output_subject = Subject()
        self.disposable = None

    async def start(self):
        loop = asyncio.get_running_loop()
        scheduler = AsyncIOScheduler(loop)

        await logger.info("🦖 MOTOR REACTIVO: Monitorizando T-Rex, Raptor y Triceratops...")

        # Flujos de datos (Configuración estandar)
        trex_heart = create_heart_stream("T-REX-01", interval_sec=1.0)
        raptor_move = create_movement_stream("RAPTOR-01", interval_sec=1.0)
        trice_temp = create_temp_stream("TRICE-01", interval_sec=2.0)

        combined_stream = rx.merge(trex_heart, raptor_move, trice_temp)

        self.disposable = combined_stream.pipe(
            # Aumentamos un poco el buffer para asegurar que capturamos
            # suficientes pasos del raptor para analizar su patrón (3 tiempos)
            ops.buffer_with_time_or_count(timespan=3.0, count=15),
            ops.filter(lambda batch: len(batch) > 0),
            ops.map(self._analyze_batch)
        ).subscribe(
            on_next=lambda data: self.output_subject.on_next(data),
            on_error=lambda e: loop.create_task(logger.error(f"❌ Error en flujo: {e}")),
            scheduler=scheduler
        )

    async def stop(self):
        if self.disposable:
            self.disposable.dispose()
            await logger.info("🛑 Sistema DETENIDO")

    def _analyze_batch(self, batch):
        alerts = []
        clean_data = []
        loop = asyncio.get_running_loop()

        raptor_moves = []

        for data in batch:
            clean_data.append(data.dict())

            # Alerta T-rex
            if data.sensor_id == "T-REX-01" and data.value > 120:
                msg = f"T-REX: Taquicardia ({data.value} bpm)"
                loop.create_task(logger.warning(msg))
                alerts.append(self._create_alert(data.sensor_id, msg, data.value))

            # Alerta triceratops
            if data.sensor_id == "TRICE-01" and data.sensor_type == "temperatura" and data.value > 40.0:
                msg = f"TRICE: Fiebre alta ({data.value}°C)"
                loop.create_task(logger.warning(msg))
                alerts.append(self._create_alert(data.sensor_id, msg, data.value))

            if data.sensor_id == "RAPTOR-01" and data.sensor_type == "movimiento":
                raptor_moves.append(data.value)

        # Alerta velociraptor
        if len(raptor_moves) >= 3:
            ultimos_movimientos = raptor_moves[-3:]
            if sum(ultimos_movimientos) == 0:
                msg = "RAPTOR: Posible Emboscada (Quieto 3 tiempos)"
                loop.create_task(logger.warning(msg))
                alert = Alert(
                    sensor_id="RAPTOR-01",
                    message=msg,
                    level="CRITICAL",
                    value_triggered=0
                )
                alerts.append(alert.dict())

        return {
            "type": "batch_update",
            "data": clean_data,
            "alerts": alerts
        }

    def _create_alert(self, sensor_id, msg, val):
        return Alert(
            sensor_id=sensor_id,
            message=msg,
            level="CRITICAL",
            value_triggered=val
        ).dict()


processor = JurassicProcessor()
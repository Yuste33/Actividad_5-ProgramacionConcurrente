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

        await logger.info("🦖 MOTOR REACTIVO: Iniciando sistema de monitorización...")

        trex_heart = create_heart_stream("T-REX-01", interval_sec=1.0)
        raptor_move = create_movement_stream("RAPTOR-01", interval_sec=1.0)
        trice_temp = create_temp_stream("TRICE-01", interval_sec=2.0)

        combined_stream = rx.merge(trex_heart, raptor_move, trice_temp)

        self.disposable = combined_stream.pipe(
            ops.buffer_with_time_or_count(timespan=2.0, count=10),
            ops.filter(lambda batch: len(batch) > 0),
            ops.map(self._analyze_batch)
        ).subscribe(
            on_next=lambda data: self.output_subject.on_next(data),
            on_error=lambda e: loop.create_task(logger.error(f" Error en flujo: {e}")),
            scheduler=scheduler
        )

    # 4. CONVERTIMOS A ASYNC
    async def stop(self):
        if self.disposable:
            self.disposable.dispose()
            await logger.info("🛑 Sistema de Monitorización: DETENIDO")

    def _analyze_batch(self, batch):
        alerts = []
        clean_data = []

        loop = asyncio.get_running_loop()

        for data in batch:
            clean_data.append(data.dict())

            if data.sensor_id == "T-REX-01" and data.value > 125:
                # logs de alerta
                loop.create_task(logger.warning(f"!! ALERTA GENERADA: Taquicardia en T-REX ({data.value})"))

                alert = Alert(
                    sensor_id=data.sensor_id,
                    message=f"ALERTA: Taquicardia detectada: {data.value}",
                    level="CRITICAL",
                    value_triggered=data.value
                )
                alerts.append(alert.dict())

        return {
            "type": "batch_update",
            "data": clean_data,
            "alerts": alerts
        }


processor = JurassicProcessor()
import asyncio
import rx
from rx import operators as ops
from rx.subject import Subject
from rx.scheduler.eventloop import AsyncIOScheduler
from app.services.stream_factory import create_movement_stream, create_temp_stream, create_heart_stream
from app.models.schemas import Alert


class JurassicProcessor:
    def __init__(self):
        self.output_subject = Subject()
        self.disposable = None

    def start(self):

        loop = asyncio.get_running_loop()
        scheduler = AsyncIOScheduler(loop)

        print("🦖 MOTOR REACTIVO ARRANCADO EN EL BUCLE CORRECTO")

        trex_heart = create_heart_stream("T-REX-01", interval_sec=0.5)
        raptor_move = create_movement_stream("RAPTOR-01", interval_sec=1.0)
        trice_temp = create_temp_stream("TRICE-01", interval_sec=2.0)

        combined_stream = rx.merge(trex_heart, raptor_move, trice_temp)

        self.disposable = combined_stream.pipe(
            ops.buffer_with_time_or_count(timespan=2.0, count=10),
            ops.filter(lambda batch: len(batch) > 0),
            ops.map(self._analyze_batch)
        ).subscribe(
            on_next=lambda data: self.output_subject.on_next(data),
            on_error=lambda e: print(f"Error en flujo: {e}"),
            scheduler=scheduler  # Usamos el scheduler sincronizado
        )

    def stop(self):
        if self.disposable:
            self.disposable.dispose()
            print("Sistema de Monitorización: DETENIDO")

    def _analyze_batch(self, batch):
        alerts = []
        clean_data = []

        for data in batch:
            clean_data.append(data.dict())

            # Lógica de Alerta
            if data.sensor_type == "cardiaco" and data.value > 110:
                alert = Alert(
                    sensor_id=data.sensor_id,
                    message=f"¡PELIGRO! Ritmo cardiaco crítico: {data.value}",
                    level="CRITICAL",
                    value_triggered=data.value
                )
                alerts.append(alert.dict())

        print(f"Lote procesado: {len(clean_data)} eventos")

        return {
            "type": "batch_update",
            "data": clean_data,
            "alerts": alerts
        }


# Instancia global
processor = JurassicProcessor()
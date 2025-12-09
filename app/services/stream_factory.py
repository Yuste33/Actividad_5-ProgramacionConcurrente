import random
import rx
from rx import operators as ops
from app.models.schemas import SensorData

def create_movement_stream(sensor_id: str, interval_sec: float = 1.0):
    return rx.interval(interval_sec).pipe(
        ops.map(lambda _: SensorData(
            sensor_type="movimiento",
            sensor_id=sensor_id,
            value=float(random.choice([0, 1])),
            unit="active"
        ))
    )

def create_temp_stream(sensor_id: str, interval_sec: float = 5.0):
    return rx.interval(interval_sec).pipe(
        ops.map(lambda _: SensorData(
            sensor_type="temperatura",
            sensor_id=sensor_id,
            value=round(random.uniform(36.5, 40.0), 1),
            unit="C"
        ))
    )

def create_heart_stream(sensor_id: str, interval_sec: float = 1.0):
    return rx.interval(interval_sec).pipe(
        ops.map(lambda _: SensorData(
            sensor_type="cardiaco",
            sensor_id=sensor_id,
            value=int(random.uniform(60, 145)),
            unit="bpm"
        ))
    )
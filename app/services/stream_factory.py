import random
import rx
from rx import operators as ops
from app.models.schemas import SensorData

def create_heart_stream(sensor_id: str, interval_sec: float = 1.0):
    return rx.interval(interval_sec).pipe(
        ops.map(lambda _: SensorData(
            sensor_type="cardiaco",
            sensor_id=sensor_id,
            # Si random < 0.1 (10%), valor critico. Si no, normal.
            value=int(random.randint(121, 150) if random.random() < 0.1 else random.randint(60, 90)),
            unit="bpm"
        ))
    )

def create_temp_stream(sensor_id: str, interval_sec: float = 5.0):
    return rx.interval(interval_sec).pipe(
        ops.map(lambda _: SensorData(
            sensor_type="temperatura",
            sensor_id=sensor_id,
            # Si random < 0.1 (10%), fiebre > 40. Si no, normal.
            value=round(random.uniform(40.1, 42.0) if random.random() < 0.1 else random.uniform(36.5, 39.0), 1),
            unit="C"
        ))
    )

def create_movement_stream(sensor_id: str, interval_sec: float = 1.0):
    return rx.interval(interval_sec).pipe(
        ops.map(lambda _: SensorData(
            sensor_type="movimiento",
            sensor_id=sensor_id,
            value=float(random.choice([0, 1])),
            unit="active"
        ))
    )
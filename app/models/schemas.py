from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime
import uuid

SensorType = Literal["movimiento", "temperatura", "cardiaco"]


class SensorData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    sensor_type: SensorType
    sensor_id: str
    value: float
    unit: str

    class Config:
        json_schema_extra = {
            "example": {
                "sensor_type": "temperatura",
                "sensor_id": "TEMP-001",
                "value": 38.5,
                "unit": "C"
            }
        }


class Alert(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    sensor_id: str
    message: str
    level: Literal["INFO", "WARNING", "CRITICAL"]
    value_triggered: float

class SystemMetrics(BaseModel):
    total_processed: int
    active_connections: int
    cpu_usage: float

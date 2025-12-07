from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.models.schemas import SystemMetrics

router = APIRouter()

request_count = 0


@router.get("/status")
async def get_system_status():
    return {
        "app": "Jurassic Park Monitor",
        "status": "OPERATIONAL",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }


@router.get("/metrics", response_model=SystemMetrics)
async def get_metrics():

    global request_count
    request_count += 1

    # Simulamos metricas del sistema
    import psutil

    return SystemMetrics(
        total_processed=request_count * 10,  # Simulado
        active_connections=1,  # Simulado
        cpu_usage=psutil.cpu_percent()
    )
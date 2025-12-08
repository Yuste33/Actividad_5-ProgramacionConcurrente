from fastapi.testclient import TestClient
from app.main import app
from app.services.processor import processor
from app.models.schemas import SensorData
from datetime import datetime

# Creamos un cliente simulado que actuara como un navegador
client = TestClient(app)


def test_status_endpoint():
    # Verifica que el servidor arranca y el endpoint /api/status responde 200 OK.

    response = client.get("/api/status")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "OPERATIONAL"
    assert "version" in json_data


def test_alert_logic_unit():
    # Simulamos un dato normal
    normal_data = SensorData(
        sensor_type="cardiaco",
        sensor_id="T-REX-01",
        value=80,
        unit="bpm",
        timestamp=datetime.now()
    )

    # Simulamos un dato CRITICO (Taquicardia)
    critical_data = SensorData(
        sensor_type="cardiaco",
        sensor_id="T-REX-01",
        value=150,  # Valor alto provocado
        unit="bpm",
        timestamp=datetime.now()
    )

    # Pasamos los datos manualmente al procesador
    batch = [normal_data, critical_data]
    result = processor._analyze_batch(batch)

    # Verificaciones
    assert len(result["data"]) == 2  # Deben estar los dos datos
    assert len(result["alerts"]) == 1  # Debe haber UNA alerta

    # Verificamos que la alerta sea correcta
    alert = result["alerts"][0]
    assert alert["level"] == "CRITICAL"
    assert "150" in alert["message"]


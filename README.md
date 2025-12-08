# Jurassic Park System: Monitorización Reactiva

Este proyecto implementa un sistema de monitorización en tiempo real para el parque jurásico, diseñado para gestionar flujos de datos concurrentes de múltiples sensores (cardíaco, movimiento, temperatura) utilizando **Programación Reactiva**.

El sistema garantiza la estabilidad bajo carga mediante técnicas de **Backpressure** y entrega datos en vivo a un dashboard web mediante **WebSockets**.

### Instalación de Dependencias

```
pip install -r requirements.txt
```

### Ejecución

```
 uvicorn app.main:app --reload
```

## Tecnologías Clave Utilizadas

* **Python 3.10+**
* **FastAPI:** Framework web asíncrono de alto rendimiento.
* **RxPY (Reactive Extensions):** Gestión de flujos de datos y eventos asíncronos.
* **Asyncio:** Concurrencia cooperativa.
* **Chart.js:** Visualización de datos en el frontend.
* **Jinja2:** Motor de plantillas para la interfaz web.

## Arquitectura del Sistema

El sistema sigue un flujo de datos unidireccional y reactivo:

1.  **Simulación (Stream Factory):** Los "sensores" generan datos periódicos simulando el comportamiento de los dinosaurios.
2.  **Procesamiento (RxPY):**
    * **Merge:** Fusiona flujos de múltiples dinosaurios en un único canal.
    * **Buffer/Backpressure:** Agrupa los datos en ventanas de tiempo (2 segundos) o cantidad (10 eventos) para evitar saturar el cliente.
    * **Análisis:** Detecta anomalías (ej. taquicardia en T-Rex > 120 bpm) y genera alertas críticas.
3.  **Distribución (WebSockets):** Los lotes procesados se envían al navegador mediante una cola asíncrona.
4.  **Visualización:** El dashboard consume el JSON y actualiza las gráficas sin recargar la página.


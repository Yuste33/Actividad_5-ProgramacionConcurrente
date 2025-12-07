from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
import asyncio
from app.services.processor import processor

router = APIRouter()


@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    queue = asyncio.Queue()

    disposable = processor.output_subject.subscribe(
        on_next=lambda data: queue.put_nowait(data)
    )

    try:
        while True:
            data = await queue.get()

            await websocket.send_json(jsonable_encoder(data))

    except WebSocketDisconnect:
        disposable.dispose()
        print("Cliente desconectado")
    except Exception as e:
        print(f"Error en WebSocket: {e}")
        disposable.dispose()
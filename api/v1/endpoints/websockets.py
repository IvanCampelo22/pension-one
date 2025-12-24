from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from api.v1.websockets.manager import ConnectionManager
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

manager = ConnectionManager()

@router.get("/")
async def websocket_page():
    base_path = Path(__file__).resolve().parents[3]
    template_path = base_path / "templates" / "websockets_templates.html"

    html = template_path.read_text(encoding="utf-8")
    return HTMLResponse(html)


@router.websocket("/ws/{client_id}")
async def websocket_handler(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left the chat")
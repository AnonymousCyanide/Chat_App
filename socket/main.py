from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from manager import UserManager , ChatManager
app = FastAPI()
user_manager = UserManager()
chat_manager = ChatManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    user_id = None

    try:
        # Initial handshake
        data = await websocket.receive_text()
        payload = json.loads(data)
        user_id = payload.get("user_id")
        chat_id = payload.get("chat_id")

        if not user_id or not chat_id:
            await websocket.send_text("Missing user_id or chat_id")
            await websocket.close()
            return

        user_manager.add_user(user_id, websocket)
        chat_manager.add_user_to_chat(user_id, chat_id)
        
        # Send chat history
        for msg in chat_manager.get_history(chat_id):
            await websocket.send_text(json.dumps(msg))

        while True:
            msg_data = await websocket.receive_text()
            msg = chat_manager.send_message(chat_id, user_id, msg_data)

            # Broadcast to other users in chat
            for peer in chat_manager.get_chat_users(chat_id):
                if True:
                    ws = user_manager.get_user_socket(peer)
                    if ws:
                        try:
                            await ws.send_text(json.dumps(msg))
                        except:
                            pass

    except WebSocketDisconnect:
        user_manager.remove_user(user_id)

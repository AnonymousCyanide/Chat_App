from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import aio_pika

app = FastAPI()

RABBITMQ_URL = "amqp://user:pass@rabbitmq/"  # Match your docker-compose credentials
QUEUE_NAME = "chat-queue"

connected_clients = set()

@app.on_event("startup")
async def startup():
    # Connect to RabbitMQ
    app.state.rabbit_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await app.state.rabbit_connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    
    # Start consuming messages from RabbitMQ and broadcasting
    async def consume():
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    for client in connected_clients:
                        await client.send_text(message.body.decode())

    asyncio.create_task(consume())
active_users = []
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Send message to RabbitMQ
            channel = await app.state.rabbit_connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(body=data.encode()),
                routing_key=QUEUE_NAME,
            )
    except WebSocketDisconnect:
        connected_clients.remove(websocket)


class User :
    def __init__(self , id : str  , websocket = None):
        self.id = id
        self.websocket = websocket
        

class Chat:
    def __init__(self, channel: str, users: list[User]):
        self.channel = channel
        self.users = users  # list of User objects
        self.messages = []  # optional: store history

    def add_message(self, sender_id: str, content: str):
        message = {
            "from": sender_id,
            "content": content
        }
        self.messages.append(message)

    def broadcast(self, sender_id: str, content: str):
        self.add_message(sender_id, content)
        for user in self.users:
            if user.is_online():
                try:
                    asyncio.create_task(
                        user.websocket.send_text(f"{sender_id}: {content}")
                    )
                except:
                    print(f"❌ Failed to send to {user.id}")

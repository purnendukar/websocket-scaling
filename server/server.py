import asyncio
import websockets
import redis.asyncio as aioredis
import os

connected = set()
redis = None
PORT = int(os.environ.get("PORT", 8001))
SERVER_NAME = os.environ.get("SERVER_NAME", f"Server-{PORT}")

async def handle_client(websocket):
    connected.add(websocket)
    try:
        async for message in websocket:
            print(f"[{SERVER_NAME}] Received: {message}")
            await redis.publish("chat", f"[{SERVER_NAME}] {message}")
    finally:
        connected.remove(websocket)

async def redis_listener():
    pubsub = redis.pubsub()
    await pubsub.subscribe("chat")
    async for msg in pubsub.listen():
        if msg["type"] == "message":
            for conn in connected:
                await conn.send(msg["data"].decode())

async def main():
    global redis
    redis = aioredis.from_url("redis://redis:6379")
    asyncio.create_task(redis_listener())
    async with websockets.serve(handle_client, "0.0.0.0", PORT):
        print(f"{SERVER_NAME} running on port {PORT}")
        await asyncio.Future()

asyncio.run(main())

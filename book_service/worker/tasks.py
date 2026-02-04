# book_service/worker/tasks.py

import asyncio
import redis.asyncio as redis

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

async def refresh_books():
    lock = await redis_client.setnx("refresh_lock", "1")
    if not lock:
        return
    await redis_client.expire("refresh_lock", 30)
    # Example task: mark refresh done
    await redis_client.set("books_last_refresh", "ok")
    await asyncio.sleep(1)  # simulate work

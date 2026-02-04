# # book_service/worker/tasks.py

# import asyncio
# import redis.asyncio as redis

# redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# async def refresh_books():
#     lock = await redis_client.setnx("refresh_lock", "1")
#     if not lock:
#         return
#     await redis_client.expire("refresh_lock", 30)
#     # Example task: mark refresh done
#     await redis_client.set("books_last_refresh", "ok")
#     await asyncio.sleep(1)  # simulate work


import time
import redis
from .main import cel  

r = redis.Redis(host='books-redis', port=6379, db=0)

@cel.task(name="refresh_catalog")
def refresh_catalog():
    lock_id = "refresh_lock"
    
    acquire_lock = r.set(lock_id, "true", ex=60, nx=True)
    
    if not acquire_lock:
        print("Refresh already in progress, skipping...")
        return "Skipped (Idempotent)"

    try:
        print("Starting background catalog refresh...")
        time.sleep(5) 
        print("Refresh completed successfully.")
        return "Success"
    finally:
 
        r.delete(lock_id)
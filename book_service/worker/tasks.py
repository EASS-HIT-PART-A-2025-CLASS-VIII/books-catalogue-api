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


import asyncio
import redis.asyncio as redis
import logging

# הגדרת לוגר למעקב (מומלץ לתיעוד ב-EX3 notes)
logger = logging.getLogger(__name__)

# חיבור ל-Redis (וודאי שה-host תואם למה שמוגדר ב-docker-compose שלך)
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

async def refresh_books():
    """
    מבצע רענון של קטלוג הספרים בצורה אידמפוטנטית.
    משתמש במנעול Redis אטומי למניעת הרצות כפולות ו-Deadlocks.
    """
    lock_key = "refresh_lock"
 
    lock_acquired = await redis_client.set(lock_key, "1", nx=True, ex=30)
    
    if not lock_acquired:
        logger.info("Refresh process skipped: Another instance is already running.")
        return {"status": "skipped", "reason": "already_running"}

    try:
        logger.info("Starting book catalogue refresh...")
        
        await redis_client.set("books_last_refresh_status", "running")

        await asyncio.sleep(5) 
        
        await redis_client.set("books_last_refresh_status", "completed")
        logger.info("Refresh completed successfully.")
        
        return {"status": "success"}

    except Exception as e:
        logger.error(f"Error during refresh: {str(e)}")
        await redis_client.set("books_last_refresh_status", "failed")
        raise e

    finally:
     
        await redis_client.delete(lock_key)
        logger.info("Refresh lock released.")



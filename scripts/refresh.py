# books-catalogue-api/scripts/refresh.py


# books-catalogue-api/scripts/refresh.py

import asyncio
import redis.asyncio as redis
import logging

logger = logging.getLogger("refresh")

LOCK_KEY = "books:refresh:lock"
RESULT_KEY = "books:last_refresh"


async def refresh_books(
    redis_client: redis.Redis,
    *,
    retries: int = 3,
    concurrency: int = 2,
    lock_ttl: int = 30,
) -> None:
    """
    Refresh books metadata.
    - Idempotent via Redis lock
    - Retries on failure
    - Bounded concurrency
    """

    for attempt in range(1, retries + 1):
        acquired = await redis_client.set(
            LOCK_KEY,
            "1",
            ex=lock_ttl,
            nx=True,
        )

        if not acquired:
            logger.info("refresh skipped (lock already held)")
            return

        try:
            semaphore = asyncio.Semaphore(concurrency)

            async def one_unit_of_work(idx: int):
                async with semaphore:
                    logger.info("refresh task %s started", idx)
                    await asyncio.sleep(0.2)  # simulate real work

            await asyncio.gather(
                *(one_unit_of_work(i) for i in range(concurrency))
            )

            await redis_client.set(RESULT_KEY, "ok")
            logger.info("refresh completed successfully")
            return

        except Exception as exc:
            logger.warning("refresh failed (attempt %s): %s", attempt, exc)
            if attempt == retries:
                raise
            await asyncio.sleep(1)

        finally:
            await redis_client.delete(LOCK_KEY)


async def main():
    client = redis.Redis(host="redis", port=6379, decode_responses=True)
    await refresh_books(client)

if __name__ == "__main__":
    asyncio.run(main())




# import asyncio
# import httpx
# import redis.asyncio as redis
# import logging

# logger = logging.getLogger("refresh")
# logging.basicConfig(level=logging.INFO)

# REDIS_URL = "redis://redis:6379/0"
# CONCURRENCY = 5
# RETRIES = 3
# KEY_PREFIX = "books:refresh:item:"

# BOOK_IDS = range(1, 21)  # Example book IDs to refresh

# r = redis.from_url(REDIS_URL, decode_responses=True)


# def idempotent_key(book_id: int) -> str:
#     return f"{KEY_PREFIX}{book_id}"


# async def refresh_book(book_id: int):
#     key = idempotent_key(book_id)
#     if await r.get(key):
#         logger.info("Skipping book %s, already refreshed", book_id)
#         return

#     for attempt in range(1, RETRIES + 1):
#         try:
#             async with httpx.AsyncClient(timeout=5.0) as client:
#                 resp = await client.get(f"http://backend:8000/books/{book_id}")
#                 resp.raise_for_status()
#                 logger.info("Book %s refreshed: %s", book_id, resp.status_code)
#                 await r.set(key, "done", ex=3600)
#                 return
#         except Exception as e:
#             logger.warning("Attempt %s failed for book %s: %s", attempt, book_id, e)
#             await asyncio.sleep(1)
#     logger.error("Failed to refresh book %s after %s retries", book_id, RETRIES)


# async def main():
#     semaphore = asyncio.Semaphore(CONCURRENCY)

#     async def sem_task(book_id: int):
#         async with semaphore:
#             await refresh_book(book_id)

#     await asyncio.gather(*(sem_task(book_id) for book_id in BOOK_IDS))


# if __name__ == "__main__":
#     asyncio.run(main())
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

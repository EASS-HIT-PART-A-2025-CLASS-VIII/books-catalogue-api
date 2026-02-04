# book_service/worker/main.py
import asyncio
from worker.tasks import refresh_books


async def main():
    while True:
        await refresh_books()
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())

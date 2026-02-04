import pytest
import redis.asyncio as redis

from scripts.refresh import refresh_books


@pytest.mark.anyio
async def test_refresh_sets_result_key():
    client = redis.Redis(host="localhost", port=6379, decode_responses=True)

    await refresh_books(client)

    value = await client.get("books:last_refresh")
    assert value == "ok"

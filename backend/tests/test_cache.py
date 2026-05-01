import pytest

from app.cache.redis_cache import (
    set_cache,
    get_cache,
    clear_paginated_posts_cache,
    tracked_paginated_posts_keys,
)

@pytest.mark.asyncio
async def test_clear_paginated_posts_cache(test_redis_client):

    keys = ["posts:page=1:size=10", "posts:page=2:size=10"]

    for key in keys:
        await set_cache(key, {"a": 1}, ttl=10, test_client=test_redis_client)

    for key in keys:
        value = await get_cache(key, test_client=test_redis_client)
        assert value == {"a": 1}

    await clear_paginated_posts_cache(test_client=test_redis_client)

    for key in keys:
        value = await get_cache(key, test_client=test_redis_client)
        assert value is None

    assert await test_redis_client.scard(tracked_paginated_posts_keys) == 0

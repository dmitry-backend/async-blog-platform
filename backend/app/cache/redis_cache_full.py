import json
import redis.asyncio as redis
from app.config import settings

# --- global variables ---
redis_client: redis.Redis | None = None
tracked_paginated_posts_keys = f"{settings.CACHE_KEY_PREFIX}:posts_pages"

# --- redis connector creation ---
async def init_redis() -> redis.Redis:
    global redis_client
    if redis_client is None:	# only create it once
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
        )
    return redis_client

# --- Cache key factories —
def create_post_id_key(post_id: int) -> str:
    return f"posts:id:{post_id}"

def create_paginated_posts_cache_key(page: int, size: int) -> str:
    return f"posts:page={page}:size={size}"


# --- Cache helpers ---
async def set_cache(
    key: str,
    value,
    ttl: int = 60,
    test_client: redis.Redis | None = None,
):

    global redis_client
    r = test_client or redis_client
    if r is None:
        r = await init_redis()

    redis_key = f"{settings.CACHE_KEY_PREFIX}:{key}"
    await r.set(redis_key, json.dumps(value), ex=ttl)

    if key.startswith("posts:page="):
        await r.sadd(tracked_paginated_posts_keys, redis_key)


async def get_cache(
    key: str,
    test_client: redis.Redis | None = None,
):

    global redis_client
    r = test_client or redis_client
    if r is None:
        r = await init_redis()

    redis_key = f"{settings.CACHE_KEY_PREFIX}:{key}"
    data = await r.get(redis_key)

    if not data:
        return None

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None

# --- Clear cache ---
async def clear_paginated_posts_cache(test_client: redis.Redis | None = None):
    global redis_client
    r = test_client or redis_client
    if r is None:
        r = await init_redis()

    keys = await r.smembers(tracked_paginated_posts_keys)
    if keys:
        await r.delete(*keys)
        await r.delete(tracked_paginated_posts_keys)

import json
import redis.asyncio as redis
from app.config import settings
from typing import Any

redis_client: redis.Redis | None = None


async def init_redis() -> redis.Redis | None:
    """Initialize Redis with safe fallback"""
    global redis_client
    
    if redis_client is not None:
        return redis_client

    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        # Test connection
        await redis_client.ping()          # ← This must be awaited
        print("✅ Redis connected successfully")
        return redis_client
    except Exception as e:
        print(f"⚠️ Redis unavailable: {e}. Running without cache.")
        redis_client = None
        return None


# Cache Key Factories
def create_post_id_key(post_id: int) -> str:
    return f"posts:id:{post_id}"


def create_paginated_posts_cache_key(page: int, size: int) -> str:
    return f"posts:page={page}:size={size}"


# Cache Operations
async def get_cache(key: str) -> Any | None:
    r = await init_redis()
    if r is None:
        return None
    try:
        data = await r.get(f"{settings.CACHE_KEY_PREFIX}:{key}")
        return json.loads(data) if data else None
    except:
        return None


async def set_cache(key: str, value: Any, ttl: int = 60) -> None:
    r = await init_redis()
    if r is None:
        return
    try:
        redis_key = f"{settings.CACHE_KEY_PREFIX}:{key}"
        await r.set(redis_key, json.dumps(value), ex=ttl)
    except:
        pass  # Silently fail if Redis is down


async def clear_paginated_posts_cache() -> None:
    """Disabled for now"""
    pass

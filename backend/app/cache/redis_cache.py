import json
import redis.asyncio as redis
from app.config import settings

redis_client: redis.Redis | None = None

async def init_redis() -> redis.Redis | None:
    """Initialize Redis with fallback if not available"""
    global redis_client
    if redis_client is not None:
        return redis_client

    try:
        redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
            socket_connect_timeout=2,   # Don't hang if Redis is missing
            socket_timeout=2,
        )
        await redis_client.ping()       # Test connection
        print("✅ Redis connected successfully")
        return redis_client
    except Exception as e:
        print(f"⚠️ Redis not available: {e}. Running without cache.")
        redis_client = None
        return None


async def get_cache(key: str):
    """Get from cache with safe fallback"""
    r = await init_redis()
    if r is None:
        return None
    
    try:
        data = await r.get(f"{settings.CACHE_KEY_PREFIX}:{key}")
        return json.loads(data) if data else None
    except:
        return None


async def set_cache(key: str, value, ttl: int = 60):
    """Set cache with safe fallback"""
    r = await init_redis()
    if r is None:
        return
    
    try:
        redis_key = f"{settings.CACHE_KEY_PREFIX}:{key}"
        await r.set(redis_key, json.dumps(value), ex=ttl)
    except:
        pass  # Silently fail if Redis is down


async def clear_paginated_posts_cache():
    pass  # Disabled for now

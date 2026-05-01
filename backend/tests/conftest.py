import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings
from app.database import get_session, Base
from app.main import app
from app.tasks.celery_app import celery_app as celery
from app.cache.redis_cache import init_redis

# --- Test database engine and session factory ---
test_engine = create_async_engine(
    settings.database_url_test,
    echo=False,
)

TestSessionMaker = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    autoflush=False,
)

# --- Create & drop tables once per test session ---
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

# --- Test Database session ---
@pytest_asyncio.fixture
async def test_db_session():
    async with TestSessionMaker() as session:
        yield session
        await session.rollback()

# --- Test HTTP client ---
@pytest_asyncio.fixture
async def test_async_client():
    async def override_get_session():
        async with TestSessionMaker() as session:
            yield session
            await session.rollback()

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()

# --- Test Redis client ---
@pytest_asyncio.fixture
async def test_redis_client():
    redis = await init_redis()
    await redis.flushdb()
    yield redis
    await redis.flushdb()
    await redis.aclose()

# --- Celery eager mode (tasks run synchronously) ---
@pytest.fixture(autouse=True)
def celery_eager():
    celery.conf.task_always_eager = True
    celery.conf.task_eager_propagates = True
    yield
    celery.conf.task_always_eager = False
    celery.conf.task_eager_propagates = False
    
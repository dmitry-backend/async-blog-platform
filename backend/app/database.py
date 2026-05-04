from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from app.config import settings
from typing import AsyncGenerator


class Base(DeclarativeBase):
    pass


# --- Engine (Optimized for Supabase Transaction Pooler) ---
engine = create_async_engine(
    settings.database_url,
    echo=settings.ENVIRONMENT == "development",
    
    # IMPORTANT for Supabase:
    poolclass=NullPool,                    # Let Supabase handle connection pooling
    pool_pre_ping=False,                   # Not needed with NullPool
    
    # These are critical for Supavisor (Supabase's pooler)
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
        "ssl": True,                       # This replaces ?sslmode=require
    },
)


# --- Session Factory ---
AsyncSessionMaker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    # class_=AsyncSession,   # already default
)


# --- Dependency for routes ---
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as session:
        yield session
        
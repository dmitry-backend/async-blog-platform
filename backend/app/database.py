import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from app.config import settings
from typing import AsyncGenerator


class Base(DeclarativeBase):
    pass


# SSL context that accepts Supabase's certificate (self-signed in pooler)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


# --- Engine (Optimized for Supabase Transaction Pooler) ---
engine = create_async_engine(
    settings.database_url,
    echo=settings.ENVIRONMENT == "development",
    
    poolclass=NullPool,                    # Critical for Supabase pooler
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
        "ssl": ssl_context,                # This fixes the certificate error
    },
)


# --- Session Factory ---
AsyncSessionMaker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


# --- Dependency for routes ---
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as session:
        yield session
        
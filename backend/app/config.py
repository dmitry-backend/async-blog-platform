from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import make_url, URL
from typing import List


class Settings(BaseSettings):
    # --- APP ---
    APP_NAME: str = "AsyncBlog API"
    ENVIRONMENT: str = "development"

    # --- LOGGING ---
    LOG_DIR: str = "logs"
    LOG_FILE: str = "app.log"

    # --- CACHE ---
    CACHE_KEY_PREFIX: str = "app"

    # --- DATABASE ---
    DATABASE_URL: str | None = None

    # Local fallback
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "async_blog"
    DB_NAME_TEST: str = "async_blog_test"

    # --- SECURITY ---
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- REDIS ---
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # --- CORS ---
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "https://async-blog-platform.onrender.com",
    ]

    # --- CELERY ---
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
    )

    @property
    def database_url(self) -> URL:
        if self.DATABASE_URL:
            url = make_url(self.DATABASE_URL)
            if url.drivername in ("postgresql", "postgres"):
                url = url.set(drivername="postgresql+asyncpg")
            return url

        # Local fallback
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )

    @property
    def database_url_sync(self) -> str:
        """For Alembic migrations"""
        if self.DATABASE_URL:
            return str(self.database_url).replace("+asyncpg", "+psycopg2")
        
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()  # type: ignore[call-arg]

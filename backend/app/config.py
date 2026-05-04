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
    JWT_SECRET_KEY: str                    # Required (must be in .env or Render)
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

    # --- Modern Pydantic v2 Config ---
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
    )

    # --- PROPERTIES ---
    @property
    def database_url(self) -> URL:
        """
        Returns a SQLAlchemy URL object.
        - On Render: uses DATABASE_URL env var
        - Locally: builds from DB_ variables
        """
        if self.DATABASE_URL:
            url = make_url(self.DATABASE_URL)

            # Force async driver for asyncpg
            if url.drivername in ("postgresql", "postgres"):
                url = url.set(drivername="postgresql+asyncpg")

            return url

        # Local fallback
        if not self.DB_USER or not self.DB_PASSWORD:
            raise ValueError(
                "DB_USER and DB_PASSWORD are required for local development. "
                "Add them to your .env file."
            )

        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )

    @property
    def database_url_test(self) -> URL:
        """For pytest"""
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME_TEST,
        )

    @property
    def database_url_sync(self) -> str:
        """Sync version if needed"""
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


# Instantiate with type ignore to silence Pylance false positive
# (Pydantic loads required fields from .env / environment variables at runtime,
# but Pylance doesn't understand this)
settings = Settings()  # type: ignore[call-arg]

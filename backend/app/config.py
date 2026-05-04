from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL
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
    DATABASE_URL: str | None = None   # Full connection string from Render

    # Fallback fields for local development
    DB_USER: str = None
    DB_PASSWORD: str = None
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

    # --- CONFIG ---
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    # --- PROPERTIES ---
    @property
    def database_url(self) -> URL:
        if self.DATABASE_URL:
            # Correct way to parse full connection string
            return URL.create(database_url=self.DATABASE_URL)
        
        # Fallback for local development
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
        return (
            f"postgresql+psycopg2://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()

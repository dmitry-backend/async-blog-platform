from celery import Celery
from app.config import settings

# --- Celery instance ---
celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

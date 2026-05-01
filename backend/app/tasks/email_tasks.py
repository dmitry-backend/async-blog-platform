import time
from app.tasks.celery_app import celery_app
from app.core.logging import logger

# --- Email task ---
@celery_app.task
def send_welcome_email(email: str):
    logger.info("Sending welcome email to %s", email)
    time.sleep(2)		# simulate email sending
    logger.info("Email sent to %s", email)

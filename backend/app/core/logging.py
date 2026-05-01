import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import settings

# --- Logs directory ---
LOG_DIR = Path(settings.LOG_DIR)
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / settings.LOG_FILE

# --- Logger ---
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Prevent duplicate logs if imported multiple times
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- Console handler ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # --- Rotating file handler ---
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5_000_000,
        backupCount=5,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

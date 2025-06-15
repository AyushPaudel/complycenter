from loguru import logger
from pathlib import Path

from app.core.config import settings

# Ensure logs directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Remove default Loguru handler to customize
logger.remove()

# Set log file path
log_file = LOG_DIR / "complycentre.log"

# Add rotating file handler
logger.add(
    log_file,
    rotation="5 MB",  # rotate after 5 MB
    retention=settings.LOG_BACKUP_COUNT,  # number of backups to keep
    level=settings.LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}",
    enqueue=True,  # for thread/process safety
)

# Add console output
logger.add(
    lambda msg: print(msg, end=""),
    level=settings.LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}",
)


def get_logger(name: str):
    return logger.bind(name=f"complycentre.{name}")

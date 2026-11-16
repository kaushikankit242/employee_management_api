
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Find the project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Create logs directory automatically
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log file location
LOG_FILE = LOG_DIR / "app.log"

# Create logger
logger = logging.getLogger("employee_management")

# Set logging level
logger.setLevel(logging.DEBUG)

# Prevent duplicate logs
logger.propagate = False

# Configure handlers only once
if not logger.handlers:

    # Define log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Display logs in terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Save logs in file with rotation
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Attach handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

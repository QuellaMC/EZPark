# app/api/utils/logger.py

import logging
from app.config.settings import settings

def setup_logger():
    logger = logging.getLogger("ezpark_backend")
    logger.setLevel(logging.INFO)

    # Create handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatters and add them to handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()

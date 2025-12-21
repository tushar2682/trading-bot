# Backend/app/utils/logger.py
import logging
import sys
import os

def setup_logger(name=__name__):
    """
    Configures a logger that outputs to console and file.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File Handler
        if not os.path.exists('logs'):
            os.makedirs('logs')
        file_handler = logging.FileHandler('logs/app.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


log = setup_logger("trading-bot")
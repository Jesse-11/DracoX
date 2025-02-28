"""
Logging utility for the Discord bot.
"""
import logging
import os
import sys
import colorlog
from logging.handlers import RotatingFileHandler

import config

def setup_logger(name):
    """
    Set up a logger with both console and file handlers.
    
    Args:
        name (str): Name of the logger
        
    Returns:
        logging.Logger: Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Create formatters
    file_formatter = logging.Formatter(config.LOG_FORMAT)
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Create file handler
    os.makedirs('logs', exist_ok=True)
    file_handler = RotatingFileHandler(
        f'logs/{config.LOG_FILE}',
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger
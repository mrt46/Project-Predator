"""
PROJECT PREDATOR - Logging Configuration
Structured logging setup
"""
import logging
import sys
from backend.core.config import config


def setup_logging():
    """Configure structured logging for the platform"""
    
    # Get log level from config
    log_level = getattr(logging, config.LOG_LEVEL, logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create logger for platform
    logger = logging.getLogger("PROJECT_PREDATOR")
    logger.setLevel(log_level)
    logger.info(f"Logging configured (level={config.LOG_LEVEL})")
    
    return logger

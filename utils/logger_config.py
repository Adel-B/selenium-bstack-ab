"""Logging configuration for the test framework."""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "selenium-bstack-ab",
    level: str = "INFO",
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Setup and configure logger with console and optional file output.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path for logging

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Set level
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_test_logger(test_name: str) -> logging.Logger:
    """Get logger for specific test.

    Args:
        test_name: Name of the test

    Returns:
        Logger instance for the test
    """
    return logging.getLogger(f"selenium-bstack-ab.{test_name}")


# Global logger instance
logger = setup_logger()

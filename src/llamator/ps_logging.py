import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(debug_level: int, artifacts_path: str):
    """
    Set up logging with a specific debug level and save logs to the provided artifacts path.

    Parameters
    ----------
    debug_level : int
        The level of logging verbosity. Allowed values:
        - 0: WARNING
        - 1: INFO
        - 2: DEBUG
    artifacts_path : str
        The path to the folder where the log file will be saved.

    Returns
    -------
    None
    """
    # Define allowed logging levels
    allowed_logging_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    logging_level = allowed_logging_levels[debug_level]

    log_file_name = "LLAMATOR_runtime.log"

    # Full path to the log file
    log_file_path = os.path.join(artifacts_path, log_file_name)

    # Create file handler with rotation and UTF-8 encoding
    file_handler = RotatingFileHandler(log_file_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
    file_handler.setLevel(logging_level)

    # Create formatter and add it to the handler
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s")
    file_handler.setFormatter(formatter)

    # Get the root logger
    root_logger = logging.getLogger()

    # Clear existing handlers to prevent logging to old files
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Add new file handler and console handler
    root_logger.addHandler(file_handler)

    # Adding a StreamHandler to output warnings and errors to stderr
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Set the overall logging level
    root_logger.setLevel(logging_level)

    logging.info(f"Logging started. Log file is saved at {log_file_path}")

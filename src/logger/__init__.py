import logging
import os
from logging.handlers import RotatingFileHandler
from from_root import from_root
from datetime import datetime

# Directory where log files will be stored
LOG_DIR = "logs"
# Log file name with current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# Maximum size of a log file before rotation (5 MB)
MAX_LOG_FILE = 5 * 1024 * 1024
# Number of backup log files to keep
BACKUP_COUNT = 3

# Full path to the log directory
log_dir_path = os.path.join(from_root(), LOG_DIR)
# Create the log directory if it doesn't exist
os.makedirs(log_dir_path, exist_ok=True)
# Full path to the log file
log_file_path = os.path.join(log_dir_path, LOG_FILE)

def configure_logger():
    # Get the root logger instance
    logger = logging.getLogger()
    # Set the logging level to DEBUG
    logger.setLevel(logging.DEBUG)

    # Define the log message format
    formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s - %(message)s")

    # Create a rotating file handler for logging to file
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=MAX_LOG_FILE,
        backupCount=BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Create a stream handler for logging to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Configure the logger when this module is imported
configure_logger()
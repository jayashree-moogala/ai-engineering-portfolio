# Import Python's built-in logging module
import logging

# Imports your application's configuration - get log level
from app.config import settings


# Initializes the logging system - configures logging for whole app - called once
def configure_logging() -> None:
    logging.basicConfig(
        # returns value for logging.<log_level> e.g logging.INFO = 20
        level=getattr(
            logging,  # logging module
            settings.log_level,  # gets value from config
            logging.INFO,  # default value
        ),
        # Format for log message -
        # Current date and time, log level, logger's name, message
        format=("%(asctime)s | %(levelname)s | " "%(name)s | %(message)s"),
    )


# creates and returns a logger
# name -> usually module name
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

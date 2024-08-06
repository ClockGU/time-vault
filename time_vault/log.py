import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)
# Get the directory containing the current file
current_directory = os.path.dirname(current_file_path)
# Go up one directory level
ROOT_DIR = os.path.dirname(current_directory)

LOG_ROOT = os.path.join(ROOT_DIR, "logs")


def get_logger():
    try:
        os.mkdir(LOG_ROOT)
    except FileExistsError:
        pass
    logger = logging.getLogger("deprovisioning")
    logger.setLevel(logging.DEBUG)
    ch = TimedRotatingFileHandler(
        os.path.join(str(LOG_ROOT), "deprovision.log"),
        when="D",
        interval=1,
        backupCount=31,
    )

    logger.addHandler(ch)
    return logger


LOGGER = get_logger()

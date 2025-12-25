import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "recognition.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("recognition_logger")
logger.setLevel(logging.INFO)

# не передаём логи наверх (в root)
logger.propagate = False

formatter = logging.Formatter(
    "%(asctime)s | %(message)s"
)

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

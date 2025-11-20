import logging
import os
from datetime import datetime
from pathlib import Path

LOG_FILE_NAME = f"log_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
LOG_DIR = Path.cwd() / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE_PATH = LOG_DIR / LOG_FILE_NAME

logging.basicConfig(
    filename=str(LOG_FILE_PATH),
    level=logging.INFO,
    format='[%(asctime)s] %(lineno)d %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_log_path() -> str:
    """Return the current log file path as a string."""
    return str(LOG_FILE_PATH)


if __name__ == "__main__":
    logging.info("Logger has been configured.")
    print(f"Log file: {LOG_FILE_PATH}")

import logging
import os 
from datetime import datetime 

LOG_FILE_NAME = f"log_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(os.getcwd(), "logs", LOG_FILE_NAME)
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

LOG_FILE_PATH = os.path.join("logs", LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='[%(asctime)s] %(lineno)d %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
if __name__ == "__main__":
    logging.info("Logger has been configured.")
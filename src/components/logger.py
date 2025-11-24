import logging
from pathlib import Path
from datetime import datetime

# Configure log directory and file using pathlib for consistency
LOG_DIR = Path.cwd() / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE_NAME = f"log_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
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
    print(f"Log file: {get_log_path()}")
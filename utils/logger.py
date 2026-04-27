# utils/logger.py

from datetime import datetime


def log(text: str):
    """
    Logs messages with timestamp into log.txt
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("log.txt", "a") as f:
        f.write(f"[{timestamp}] {text}\n")
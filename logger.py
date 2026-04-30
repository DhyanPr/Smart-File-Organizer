import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "log.txt")

def log(message):
    os.makedirs(LOG_DIR, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:  # ✅ FIX
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{time_stamp}] {message}\n")
import os

DEBUG_LOG_PATH = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(DEBUG_LOG_PATH, exist_ok=True)
DEBUG_LOG_FILE = os.path.join(DEBUG_LOG_PATH, "rag_debug.log")


def log_debug(message):
    """Write debug message to log file and console"""
    print(f"[RAG DEBUG] {message}")
    with open(DEBUG_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")
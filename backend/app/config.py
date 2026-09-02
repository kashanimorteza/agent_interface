import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_URL = f"sqlite:///{BASE_DIR / 'trading_assistant.db'}"

API_KEY = os.getenv("API_KEY", "dev-api-key")

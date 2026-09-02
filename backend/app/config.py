"""Configuration read from the environment — nothing here is hard-coded."""
import os

DATABASE_PATH: str = os.environ.get("DATABASE_PATH", "app.db")
DATABASE_URL: str = f"sqlite:///{DATABASE_PATH}"
API_KEY: str | None = os.environ.get("API_KEY")

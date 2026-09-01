import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings

assert settings.database_path.parts[-2:] == ("data", "app.db")
print("T7 OK")

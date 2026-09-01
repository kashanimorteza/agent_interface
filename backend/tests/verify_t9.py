import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app

assert app.docs_url == "/docs", f"docs_url={app.docs_url}, expected /docs"
assert app.redoc_url is None, f"redoc_url={app.redoc_url}, expected None"
print("T9 OK")

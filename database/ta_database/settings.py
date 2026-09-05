"""Runtime settings for the Database Component.

Values come from the process environment, optionally topped up from an
untracked ``.env`` file beside this package. Nothing here is committed
with a secret; the encryption key is read at call time and never defaulted.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ENV_DATABASE_URL = "TA_DATABASE_URL"
ENV_ENCRYPTION_KEY = "TA_DATABASE_ENCRYPTION_KEY"

_PACKAGE_DIR = Path(__file__).resolve().parent
_COMPONENT_DIR = _PACKAGE_DIR.parent
_DEFAULT_DB_FILE = _COMPONENT_DIR / "app.db"
_ENV_FILE = _COMPONENT_DIR / ".env"


@dataclass(frozen=True)
class Settings:
    database_url: str
    encryption_key: str | None


def _read_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key:
            values[key] = value
    return values


def _lookup(name: str, file_values: dict[str, str]) -> str | None:
    value = os.environ.get(name)
    if value is None:
        value = file_values.get(name)
    if value is not None and value.strip() == "":
        return None
    return value


def default_database_url() -> str:
    return f"sqlite:///{_DEFAULT_DB_FILE.as_posix()}"


def get_settings() -> Settings:
    file_values = _read_env_file(_ENV_FILE)
    url = _lookup(ENV_DATABASE_URL, file_values) or default_database_url()
    key = _lookup(ENV_ENCRYPTION_KEY, file_values)
    return Settings(database_url=url, encryption_key=key)

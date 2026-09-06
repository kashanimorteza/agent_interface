"""Runtime configuration of the Database Component.

Connection settings and the credential encryption key come from runtime configuration only
(process environment first, then an untracked ``.env`` file in the Database code root, then the
resolved default), never from committed files.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

ENV_DATABASE_URL = "DATABASE_URL"
ENV_CREDENTIAL_ENCRYPTION_KEY = "CREDENTIAL_ENCRYPTION_KEY"
DEFAULT_DATABASE_FILENAME = "app.db"
ENV_FILENAME = ".env"


@dataclass(frozen=True)
class Settings:
    database_url: str
    credential_encryption_key: str | None


def code_root() -> Path:
    """The Database code root: the nearest ancestor containing pyproject.toml, else the working directory."""
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "pyproject.toml").is_file():
            return candidate
    return Path.cwd().resolve()


def _parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def get_settings(*, environ: Mapping[str, str] | None = None, load_env_file: bool = True) -> Settings:
    """Resolve settings: given environ (default os.environ), then .env in the code root, then defaults."""
    source: dict[str, str] = dict(os.environ if environ is None else environ)
    if load_env_file:
        for key, value in _parse_env_file(code_root() / ENV_FILENAME).items():
            source.setdefault(key, value)
    url = source.get(ENV_DATABASE_URL, "").strip()
    if not url:
        url = f"sqlite:///{(code_root() / DEFAULT_DATABASE_FILENAME).as_posix()}"
    key = source.get(ENV_CREDENTIAL_ENCRYPTION_KEY, "").strip() or None
    return Settings(database_url=url, credential_encryption_key=key)

"""Runtime configuration of the Backend Component (process environment, then an untracked .env, then defaults)."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

ENV_HOST = "BACKEND_HOST"
ENV_PORT = "BACKEND_PORT"
ENV_CORS_ORIGINS = "BACKEND_CORS_ORIGINS"
ENV_FILENAME = ".env"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_CORS_ORIGINS = ("http://127.0.0.1:3000", "http://localhost:3000")


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    cors_origins: tuple[str, ...]


def code_root() -> Path:
    """The Backend code root: the nearest ancestor containing pyproject.toml, else the working directory."""
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
    host = source.get(ENV_HOST, "").strip() or DEFAULT_HOST
    raw_port = source.get(ENV_PORT, "").strip()
    try:
        port = int(raw_port) if raw_port else DEFAULT_PORT
    except ValueError:
        raise ValueError(f"{ENV_PORT} must be an integer port number, got {raw_port!r}") from None
    if not 0 < port < 65536:
        raise ValueError(f"{ENV_PORT} must be between 1 and 65535, got {port}")
    raw_origins = source.get(ENV_CORS_ORIGINS, "").strip()
    origins = tuple(o.strip() for o in raw_origins.split(",") if o.strip()) if raw_origins else DEFAULT_CORS_ORIGINS
    return Settings(host=host, port=port, cors_origins=origins)

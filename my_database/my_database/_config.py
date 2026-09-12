"""Resolves Database's layer-local runtime configuration and file locations.

Storage paths are resolved from this Component's own package location rather
than assumed parent-directory hops, so resolution stays correct whether the
package is installed editable (development) or as a regular dependency.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_PACKAGE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT_CANDIDATE = _PACKAGE_DIR.parent

# Prefer the project root (so data/ and .secrets/ sit next to pyproject.toml,
# matching code_path) only when it is actually present; otherwise fall back
# to the installed package directory itself. This avoids assuming a fixed
# number of parent hops that a non-editable install could flatten away.
CODE_PATH = (
    _PROJECT_ROOT_CANDIDATE
    if (_PROJECT_ROOT_CANDIDATE / "pyproject.toml").is_file()
    else _PACKAGE_DIR
)

DATA_DIR = CODE_PATH / "data"
SECRETS_DIR = CODE_PATH / ".secrets"
_CONFIG_FILE = _PACKAGE_DIR / "database.yaml"


def load_runtime_configuration() -> dict[str, Any]:
    with _CONFIG_FILE.open(encoding="utf-8") as handle:
        config: dict[str, Any] = yaml.safe_load(handle)
    return config

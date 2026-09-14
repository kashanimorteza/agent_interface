"""Resolves Database's component root directory: where `database.yaml`, `data/`, and
`.secrets/` live.

A regular (non-editable) install of this package into a consumer's virtual environment
(for example, when Backend depends on Database) copies its files into that consumer's
`site-packages`, which is not the original component root. `DATABASE_COMPONENT_ROOT` lets
the deploying environment tell Database where its actual component root is; this is
exactly the kind of environment-specific Runtime Binding Platform is expected to supply.
When unset, Database resolves its root relative to its own installed file location, which
is correct for Database's own development, tests, and any editable install.
"""

from __future__ import annotations

import os
from pathlib import Path

_ENV_VAR = "DATABASE_COMPONENT_ROOT"
_FILE_RELATIVE_ROOT = Path(__file__).resolve().parents[2]


def component_root() -> Path:
    override = os.environ.get(_ENV_VAR)
    if override:
        return Path(override).expanduser().resolve()
    return _FILE_RELATIVE_ROOT

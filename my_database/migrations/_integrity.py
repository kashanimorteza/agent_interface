"""Integrity markers for the migration history (Database Standard 2.15).

Internal migration tooling — not part of the public Database Interface.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

VERSIONS_DIR = Path(__file__).parent / "versions"
MANIFEST_PATH = Path(__file__).parent / "integrity.json"


def _checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _revision_files() -> list[Path]:
    return sorted(p for p in VERSIONS_DIR.glob("*.py") if p.stem != "__init__")


def write_manifest() -> dict[str, str]:
    """(Re)compute and persist the checksum of every migration file."""
    manifest = {p.stem: _checksum(p) for p in _revision_files()}
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def verify_manifest() -> list[str]:
    """Return the revision file names whose content no longer matches the recorded checksum."""
    if not MANIFEST_PATH.exists():
        return []
    recorded = json.loads(MANIFEST_PATH.read_text())
    mismatched = []
    for path in _revision_files():
        expected = recorded.get(path.stem)
        if expected is not None and expected != _checksum(path):
            mismatched.append(path.stem)
    return mismatched

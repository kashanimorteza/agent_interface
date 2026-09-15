"""Migration execution: ordering, integrity, drift detection, and reproducibility.

Application code never creates, alters, or drops storage objects directly;
every structural change happens through this module's recorded, ordered
Alembic Migration history.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from alembic.config import Config
from sqlalchemy import inspect
from sqlalchemy.engine import Connection, Engine

from alembic import command
from database import observability
from database.mapping import build_metadata

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
ALEMBIC_INI = COMPONENT_ROOT / "alembic.ini"
ALEMBIC_DIR = COMPONENT_ROOT / "alembic"
VERSIONS_DIR = ALEMBIC_DIR / "versions"
CHECKSUM_MANIFEST = VERSIONS_DIR / "checksums.json"


def _alembic_config(connection: Connection) -> Config:
    cfg = Config(str(ALEMBIC_INI))
    cfg.set_main_option("script_location", str(ALEMBIC_DIR))
    cfg.attributes["connection"] = connection
    return cfg


def upgrade_to_head(engine: Engine) -> None:
    """Apply every recorded Migration, in order, up to head."""
    with engine.begin() as connection:
        try:
            command.upgrade(_alembic_config(connection), "head")
        except Exception as error:
            observability.record_migration_failure("head", error)
            raise


def downgrade_to_base(engine: Engine) -> None:
    """Reverse every recorded Migration back to an empty schema; the tested reversal path."""
    with engine.begin() as connection:
        try:
            command.downgrade(_alembic_config(connection), "base")
        except Exception as error:
            observability.record_migration_failure("base", error)
            raise


def _script_files() -> list[Path]:
    return sorted(p for p in VERSIONS_DIR.glob("*.py") if p.name != "__init__.py")


def compute_checksums() -> dict[str, str]:
    """Compute the current integrity checksum of every recorded Migration script."""
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in _script_files()}


def write_checksum_manifest() -> None:
    """Record the current Migration checksums as the integrity baseline (run after adding a Migration)."""
    CHECKSUM_MANIFEST.write_text(
        json.dumps(compute_checksums(), indent=2, sort_keys=True) + "\n"
    )


def verify_migration_integrity() -> list[str]:
    """Return every mismatch between the recorded and current Migration-file checksums; empty means intact."""
    if not CHECKSUM_MANIFEST.is_file():
        return [
            "No checksum manifest recorded; run write_checksum_manifest() after generating migrations."
        ]
    recorded: dict[str, str] = json.loads(CHECKSUM_MANIFEST.read_text())
    current = compute_checksums()
    mismatches: list[str] = []
    for name, checksum in recorded.items():
        if name not in current:
            mismatches.append(f"missing migration file: {name}")
        elif current[name] != checksum:
            mismatches.append(f"checksum mismatch: {name}")
    for name in current:
        if name not in recorded:
            mismatches.append(f"unrecorded migration file: {name}")
    return mismatches


def detect_schema_drift(engine: Engine) -> list[str]:
    """Compare the running structure against the recorded mapping; empty list means no drift."""
    inspector = inspect(engine)
    expected = build_metadata()
    drift: list[str] = []
    existing_tables = set(inspector.get_table_names())
    for table in expected.sorted_tables:
        if table.name not in existing_tables:
            drift.append(f"missing table: {table.name}")
            continue
        existing_columns = {c["name"] for c in inspector.get_columns(table.name)}
        expected_columns = {c.name for c in table.columns}
        for missing in expected_columns - existing_columns:
            drift.append(f"missing column: {table.name}.{missing}")
        for extra in existing_columns - expected_columns:
            drift.append(f"unexpected column: {table.name}.{extra}")
    return drift


def ensure_ready(engine: Engine) -> None:
    """Verify Migration integrity, apply every pending Migration, and confirm no structural drift remains.

    Called once at startup (startup_schema_creation); raises on any
    unresolved integrity or drift problem instead of silently proceeding.
    """
    integrity_problems = verify_migration_integrity()
    if integrity_problems:
        msg = f"Migration integrity check failed: {'; '.join(integrity_problems)}"
        raise RuntimeError(msg)
    upgrade_to_head(engine)
    drift = detect_schema_drift(engine)
    if drift:
        msg = f"Schema drift detected after Migration: {'; '.join(drift)}"
        raise RuntimeError(msg)

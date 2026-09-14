"""Programmatic access to Database's ordered Migration history."""

from __future__ import annotations

from alembic import command
from alembic.config import Config

from . import observability
from .exceptions import MigrationFailure
from .paths import component_root


def _alembic_config(*, instance: str | None, db_url: str | None) -> Config:
    root = component_root()
    cfg = Config(str(root / "alembic.ini"))
    cfg.set_main_option("script_location", str(root / "migrations"))
    if db_url:
        cfg.set_main_option("sqlalchemy.url", db_url)
    elif instance:
        cfg.set_main_option("database_instance", instance)
    return cfg


def upgrade_to_head(*, instance: str | None = None, db_url: str | None = None) -> None:
    """Apply every unapplied Migration for the selected Database Instance."""
    try:
        command.upgrade(_alembic_config(instance=instance, db_url=db_url), "head")
    except Exception as exc:
        observability.migration_failure(exc.__class__.__name__)
        raise MigrationFailure("Failed to apply the Migration history") from exc


def downgrade_to_base(*, instance: str | None = None, db_url: str | None = None) -> None:
    """Reverse every applied Migration for the selected Database Instance."""
    try:
        command.downgrade(_alembic_config(instance=instance, db_url=db_url), "base")
    except Exception as exc:
        observability.migration_failure(exc.__class__.__name__)
        raise MigrationFailure("Failed to reverse the Migration history") from exc

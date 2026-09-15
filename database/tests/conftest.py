from __future__ import annotations

from pathlib import Path

import pytest
from cryptography.fernet import Fernet


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Every test gets an ephemeral SQLite file under tmp_path, never the
    committed database/data/ location, and a fresh generated encryption key.
    """
    monkeypatch.setenv("DATABASE_ENCRYPTION_KEY", Fernet.generate_key().decode())

    import database.config as config_module

    monkeypatch.setattr(config_module, "DATA_DIR", tmp_path)

    import database.bootstrap as bootstrap_module

    bootstrap_module.reset_readiness_cache()
    yield
    bootstrap_module.reset_readiness_cache()

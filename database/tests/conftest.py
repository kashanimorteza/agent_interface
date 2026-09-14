import os

import pytest
from cryptography.fernet import Fernet
from sqlalchemy import create_engine, event
from sqlalchemy.pool import StaticPool

from database import (  # noqa: F401  (mapping import registers every ORM class)
    adapter,
    mapping,
)
from database.foundation import StorageBase


@pytest.fixture(autouse=True, scope="session")
def _encryption_key() -> None:
    os.environ.setdefault("DATABASE_ENCRYPTION_KEY", Fernet.generate_key().decode())


@pytest.fixture(autouse=True)
def _isolated_engine(monkeypatch: pytest.MonkeyPatch) -> None:
    engine = create_engine(
        "sqlite:///:memory:",
        future=True,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection, connection_record):  # type: ignore[no-untyped-def]
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    StorageBase.metadata.create_all(engine)
    monkeypatch.setattr(adapter, "_engines", {adapter.default_instance(): engine})

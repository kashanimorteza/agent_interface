"""The explicit Transaction boundary: related operations on one Database Instance commit or
roll back together; a standalone write forms its own atomic unit."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from . import observability
from .adapter import StorageAdapter
from .exceptions import TransactionConflict


@dataclass(slots=True)
class Transaction:
    """One grouped unit of operations on a single Database Instance."""

    session: Session
    instance_key: str


@contextmanager
def transaction(adapter: StorageAdapter) -> Iterator[Transaction]:
    session = adapter.session()
    txn = Transaction(session=session, instance_key=adapter.instance.key)
    try:
        yield txn
        session.commit()
    except OperationalError as exc:
        session.rollback()
        observability.transaction_conflict(adapter.instance.key, exc.__class__.__name__)
        raise TransactionConflict("Transaction conflict detected; unit rolled back") from exc
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

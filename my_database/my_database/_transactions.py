"""The explicit transaction boundary: groups related generic operations on
one Instance so they commit together or roll back together.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from my_database._errors import ConstraintViolationError, TransactionConflictError
from my_database._session import get_session_factory

_TRANSIENT_MARKERS = ("database is locked", "deadlock", "serialization")


@contextmanager
def transaction(instance: str | None = None) -> Iterator[Session]:
    """Group related generic operations on one Instance in one atomic unit.

    Every change made through the yielded session commits together only if
    the block completes without raising; any exception rolls back every
    change the group made.
    """

    session_factory = get_session_factory(instance)
    session = session_factory()
    try:
        yield session
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise ConstraintViolationError(str(error.orig)) from error
    except OperationalError as error:
        session.rollback()
        message = str(error.orig).lower()
        if any(marker in message for marker in _TRANSIENT_MARKERS):
            raise TransactionConflictError(str(error.orig)) from error
        raise
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

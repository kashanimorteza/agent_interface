"""The transaction boundary: groups related generic operations into one commit or rollback."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy.exc import DBAPIError, OperationalError

from . import _session
from .exceptions import ConnectionFailure, TransactionConflict, TransactionTimeout


class Unit:
    """One transactional unit bound to a single resolved Instance.

    Pass the same :class:`Unit` to every :mod:`my_database.operations` call
    that must commit or roll back together. A standalone operation call made
    without a ``Unit`` forms its own atomic unit.
    """

    def __init__(self, instance_key: str | None):
        self.session = _session.session_for(instance_key)


@contextmanager
def unit(instance: str | None = None) -> Iterator[Unit]:
    """Group related operations on one Instance into one commit-or-rollback unit.

    Example::

        with my_database.transactions.unit() as tx:
            my_database.operations.add(my_model.Broker, unit=tx, name="X", user_id=1)
            my_database.operations.add(my_model.Broker, unit=tx, name="Y", user_id=1)
        # both committed together, or neither if any step raised
    """
    tx = Unit(instance)
    try:
        yield tx
        tx.session.commit()
    except OperationalError as error:
        tx.session.rollback()
        message = str(error).lower()
        if "lock" in message or "busy" in message:
            raise TransactionConflict(str(error)) from error
        if "timeout" in message:
            raise TransactionTimeout(str(error)) from error
        raise ConnectionFailure(str(error)) from error
    except DBAPIError as error:
        tx.session.rollback()
        raise ConnectionFailure(str(error)) from error
    except Exception:
        tx.session.rollback()
        raise
    finally:
        tx.session.close()

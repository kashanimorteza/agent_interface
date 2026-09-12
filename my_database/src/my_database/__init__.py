"""my_database — the complete persistence layer for the Trading Assistant.

Consumers reach every capability through these public modules:

    import my_database
    my_database.operations.add(my_model.Broker, name="X", user_id=1)
    my_database.registry.list_instances()
    with my_database.transactions.unit() as tx:
        ...
    my_database.sql.execute("select * from brokers where user_id = :uid", {"uid": 1})

No connection object, ORM mapping, or secret value is exposed through this
public interface.
"""

from __future__ import annotations

from . import exceptions, operations, registry, sql, transactions
from ._seed import seed_all as seed

__all__ = [
    "exceptions",
    "operations",
    "registry",
    "sql",
    "transactions",
    "seed",
]

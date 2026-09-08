"""The persistence layer of Trading Assistant.

This package stores the shared domain definitions and publishes one way of
reaching them. A consumer works with the definitions it already knows — the
entities the Model layer publishes — and this layer works out how each is held,
what its rules require, and where the data actually lives.

What this publishes:

* ``Database`` — the gateway: create, read, list, update, delete, enable and
  disable for every definition; a boundary that holds related changes together;
  and a controlled route for the little that cannot be said as an operation.
* ``InstanceRegistry`` — which stored identities exist and which is used when a
  caller names none.

What it does not publish, deliberately: the engine, the connection, the mapping,
and the recorded history of the structure. Those are how the promises above are
kept, and a consumer that depended on them would be depending on something this
layer never agreed to keep still.
"""

from .interface import (
    DISABLE,
    ENABLE,
    CommandRefused,
    CommandResult,
    ConfigurationError,
    Database,
    InstanceIdentity,
    InstanceRegistry,
    OperationError,
    Transaction,
    TransactionCancelled,
)

__version__ = "0.1.0"

__all__ = [
    "DISABLE",
    "ENABLE",
    "CommandRefused",
    "CommandResult",
    "ConfigurationError",
    "Database",
    "InstanceIdentity",
    "InstanceRegistry",
    "OperationError",
    "Transaction",
    "TransactionCancelled",
    "__version__",
]

"""Database — the Trading Assistant's persistence boundary.

Public Interface: the generic Database Interface (create, get_by_id, list_,
search, update, delete, enable, disable), the explicit Transaction boundary,
the capability-restricted controlled-command route, and the Instance
Registry. Private internal organization (config, mapping, credentials,
migrations, integrity, bootstrap) may change without notice.
"""

from database.exceptions import (
    ActivationNotSupportedError,
    ControlledCommandRejectedError,
    DatabaseConfigurationError,
    SchemaDriftError,
    UnknownInstanceError,
    UnsupportedCredentialModeError,
)
from database.initial_data import import_initial_data
from database.interface import (
    Transaction,
    create,
    delete,
    disable,
    enable,
    execute_command,
    get_by_id,
    list_,
    search,
    transaction,
    update,
)
from database.registry import InstanceIdentity, InstanceRegistry, instance_registry

__all__ = [
    "ActivationNotSupportedError",
    "ControlledCommandRejectedError",
    "DatabaseConfigurationError",
    "InstanceIdentity",
    "InstanceRegistry",
    "SchemaDriftError",
    "Transaction",
    "UnknownInstanceError",
    "UnsupportedCredentialModeError",
    "create",
    "delete",
    "disable",
    "enable",
    "execute_command",
    "get_by_id",
    "import_initial_data",
    "instance_registry",
    "list_",
    "search",
    "transaction",
    "update",
]

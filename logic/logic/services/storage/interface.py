"""Storage Service Interface: the gateway and the Database contracts a Service needs, republished unchanged."""

from database.interface import (
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
)

from logic.services.storage.core import Storage

__all__ = [
    "CommandResult",
    "ConfigurationError",
    "ConnectionFailureError",
    "DatabaseError",
    "DatabaseInstance",
    "DeclarationMismatchError",
    "ExecutionError",
    "Filter",
    "FilterCombination",
    "FilterOperator",
    "InactiveInstanceError",
    "InvalidInputError",
    "LifecycleError",
    "LifecycleResult",
    "Order",
    "OrderDirection",
    "Storage",
]

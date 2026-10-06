"""The Storage Service Interface: the gateway and the republished Database contracts."""

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
    "Storage",
    "ConfigurationError",
    "ConnectionFailureError",
    "DatabaseError",
    "DeclarationMismatchError",
    "ExecutionError",
    "InactiveInstanceError",
    "InvalidInputError",
    "LifecycleError",
    "CommandResult",
    "DatabaseInstance",
    "Filter",
    "FilterCombination",
    "FilterOperator",
    "LifecycleResult",
    "Order",
    "OrderDirection",
]

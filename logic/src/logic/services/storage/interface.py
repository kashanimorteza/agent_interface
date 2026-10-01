"""Storage Service Interface: Logic's internal gateway to every Database capability."""

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

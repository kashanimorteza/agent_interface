"""The Storage Service Interface: the gateway and every Database contract it needs."""

from database.interface import CommandResult as CommandResult
from database.interface import ConfigurationError as ConfigurationError
from database.interface import ConnectionFailureError as ConnectionFailureError
from database.interface import DatabaseError as DatabaseError
from database.interface import DatabaseInstance as DatabaseInstance
from database.interface import DeclarationMismatchError as DeclarationMismatchError
from database.interface import ExecutionError as ExecutionError
from database.interface import Filter as Filter
from database.interface import FilterCombination as FilterCombination
from database.interface import FilterOperator as FilterOperator
from database.interface import InactiveInstanceError as InactiveInstanceError
from database.interface import InvalidInputError as InvalidInputError
from database.interface import LifecycleError as LifecycleError
from database.interface import LifecycleResult as LifecycleResult
from database.interface import Order as Order
from database.interface import OrderDirection as OrderDirection

from logic.services.storage.core import Storage as Storage

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

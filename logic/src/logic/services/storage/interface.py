"""Storage Service Interface: one Action for every Database Operation and the Instance Enum."""

from database.interface import Database as _Database
from database.interface import DatabaseInstance

from logic.core.settings import STORAGE as _STORAGE
from logic.services.storage.actions.storage_add import storage_add
from logic.services.storage.actions.storage_count import storage_count
from logic.services.storage.actions.storage_create_tables import storage_create_tables
from logic.services.storage.actions.storage_delete import storage_delete
from logic.services.storage.actions.storage_disable import storage_disable
from logic.services.storage.actions.storage_enable import storage_enable
from logic.services.storage.actions.storage_execute_command import (
    storage_execute_command,
)
from logic.services.storage.actions.storage_get_by_id import storage_get_by_id
from logic.services.storage.actions.storage_insert_initial_data import (
    storage_insert_initial_data,
)
from logic.services.storage.actions.storage_list import storage_list
from logic.services.storage.actions.storage_max import storage_max
from logic.services.storage.actions.storage_min import storage_min
from logic.services.storage.actions.storage_sum import storage_sum
from logic.services.storage.actions.storage_truncate import storage_truncate
from logic.services.storage.actions.storage_update import storage_update
from logic.services.storage.catalogue import derive as _derive

__all__ = [
    "DatabaseInstance",
    "storage_add",
    "storage_count",
    "storage_create_tables",
    "storage_delete",
    "storage_disable",
    "storage_enable",
    "storage_execute_command",
    "storage_get_by_id",
    "storage_insert_initial_data",
    "storage_list",
    "storage_max",
    "storage_min",
    "storage_sum",
    "storage_truncate",
    "storage_update",
]

_ACTIONS = _derive(_Database, _STORAGE, reserved=("DatabaseInstance",))
for _stale in [n for n in __all__ if n != "DatabaseInstance" and n not in _ACTIONS]:
    __all__.remove(_stale)
    del globals()[_stale]
for _name, _action in _ACTIONS.items():
    globals()[_name] = _action
    if _name not in __all__:
        __all__.append(_name)

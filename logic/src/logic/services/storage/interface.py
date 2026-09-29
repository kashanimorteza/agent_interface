"""Storage Service Interface: every Storage Action and the exact Database Instance Enum."""

from database.interface import DatabaseInstance
from logic.services.storage.actions.storage_add import storage_add
from logic.services.storage.actions.storage_update import storage_update
from logic.services.storage.actions.storage_list import storage_list
from logic.services.storage.actions.storage_delete import storage_delete
from logic.services.storage.actions.storage_enable import storage_enable
from logic.services.storage.actions.storage_disable import storage_disable
from logic.services.storage.actions.storage_get_by_id import storage_get_by_id
from logic.services.storage.actions.storage_count import storage_count
from logic.services.storage.actions.storage_sum import storage_sum
from logic.services.storage.actions.storage_min import storage_min
from logic.services.storage.actions.storage_max import storage_max
from logic.services.storage.actions.storage_truncate import storage_truncate
from logic.services.storage.actions.storage_execute_command import (
    storage_execute_command,
)
from logic.services.storage.actions.storage_create_tables import storage_create_tables
from logic.services.storage.actions.storage_insert_initial_data import (
    storage_insert_initial_data,
)

__all__ = [
    "DatabaseInstance",
    "storage_add",
    "storage_update",
    "storage_list",
    "storage_delete",
    "storage_enable",
    "storage_disable",
    "storage_get_by_id",
    "storage_count",
    "storage_sum",
    "storage_min",
    "storage_max",
    "storage_truncate",
    "storage_execute_command",
    "storage_create_tables",
    "storage_insert_initial_data",
]

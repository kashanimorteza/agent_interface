"""Database's Public Interface.

The only Database boundary published to consumers: the generic Model-driven
Database Interface, the Transaction boundary, the Instance Registry, and
Migration/readiness operations. Consumers never import a private adapter,
mapping, connection, or configuration file.
"""

from database.adapter import (
    InstanceConfigurationError,
    StorageAdapter,
    UnknownInstanceError,
)
from database.interface import (
    ActivationNotSupportedError,
    DatabaseInterface,
    RecordNotFoundError,
    Transaction,
    UnknownControlledCommandError,
    UnknownDomainDefinitionError,
    UnknownSearchFieldError,
)
from database.mapping import portability_report
from database.migrations import (
    detect_schema_drift,
    downgrade_to_base,
    ensure_ready,
    upgrade_to_head,
    verify_migration_integrity,
    write_checksum_manifest,
)
from database.registry import InstanceDescriptor, InstanceRegistry

__all__ = [
    "ActivationNotSupportedError",
    "DatabaseInterface",
    "InstanceConfigurationError",
    "InstanceDescriptor",
    "InstanceRegistry",
    "RecordNotFoundError",
    "StorageAdapter",
    "Transaction",
    "UnknownControlledCommandError",
    "UnknownDomainDefinitionError",
    "UnknownInstanceError",
    "UnknownSearchFieldError",
    "detect_schema_drift",
    "downgrade_to_base",
    "ensure_ready",
    "portability_report",
    "upgrade_to_head",
    "verify_migration_integrity",
    "write_checksum_manifest",
]

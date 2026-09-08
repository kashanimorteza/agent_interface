"""The shared domain Model layer of Trading Assistant.

This is the one place the project says what its entities are. Every layer that
works with domain data reads those entities from here rather than keeping its
own copy, so persistence, application logic and presentation all mean the same
thing by a User, an Account or a Position.

What this package publishes:

* the entities themselves, each with its fields, connections and rules;
* the records the project must contain when it begins, and the order they
  resolve in;
* the declaration types those are expressed with, for a consumer that needs to
  read a definition rather than an instance.

What it does not do: it stores nothing, calls nothing, and enforces no rule it
cannot judge from an entity's own values. A rule needing stored records or an
operation's context is declared here and enforced by the layer that has them.
"""

from .entities import (
    ENTITIES,
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from .foundation import (
    GENERATE_SECURELY,
    UNSET,
    Cardinality,
    CredentialStorage,
    DomainRule,
    Entity,
    FieldSpec,
    FieldType,
    Generated,
    InitialRecord,
    PartialView,
    Relationship,
    RuleScope,
    awaits_generation,
    is_stated,
)
from .records import (
    declared_records,
    entities_with_records,
    records_in_resolution_order,
    references_of,
    resolution_order,
    unresolved_references,
)

__version__ = "0.1.0"

__all__ = [
    # <!-------------------------------------------- entities -->
    "ENTITIES",
    "Account",
    "AccountGroup",
    "Action",
    "ActionGroup",
    "Asset",
    "Broker",
    "Currency",
    "PartialGroup",
    "PartialRule",
    "Position",
    "TradingPlatform",
    "TrailingGroup",
    "TrailingRule",
    "User",
    # <!-------------------------------------------- declarations -->
    "Cardinality",
    "CredentialStorage",
    "DomainRule",
    "Entity",
    "FieldSpec",
    "FieldType",
    "GENERATE_SECURELY",
    "Generated",
    "InitialRecord",
    "PartialView",
    "Relationship",
    "RuleScope",
    "UNSET",
    "awaits_generation",
    "is_stated",
    # <!-------------------------------------------- records -->
    "declared_records",
    "entities_with_records",
    "records_in_resolution_order",
    "references_of",
    "resolution_order",
    "unresolved_references",
    "__version__",
]

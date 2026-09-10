"""Public import interface of the Model package.

Consumers import Models, their declarations, and their initial records from this
module only; everything else in the package is internal.
"""

from my_model._catalog import (
    MODELS,
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    Instance,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
    initial_records,
)
from my_model._declarations import (
    NOT_DECLARED,
    AtRestMode,
    AwaitingGeneration,
    Cardinality,
    DomainModel,
    FieldDeclaration,
    GenerationMethod,
    LogicalType,
    Participation,
    Relationship,
    RelationshipKind,
    RuleDeclaration,
    RuleKind,
    RuleRequirement,
)

__all__ = [
    # Models, in project-definition order
    "User",
    "TradingPlatform",
    "Currency",
    "Broker",
    "Asset",
    "Instance",
    "AccountGroup",
    "Account",
    "TrailingGroup",
    "TrailingRule",
    "PartialGroup",
    "PartialRule",
    "ActionGroup",
    "Action",
    "Position",
    # Catalogue and initial records
    "MODELS",
    "initial_records",
    # Declarations
    "DomainModel",
    "FieldDeclaration",
    "LogicalType",
    "NOT_DECLARED",
    "AtRestMode",
    "GenerationMethod",
    "AwaitingGeneration",
    "Relationship",
    "RelationshipKind",
    "Cardinality",
    "Participation",
    "RuleDeclaration",
    "RuleKind",
    "RuleRequirement",
]

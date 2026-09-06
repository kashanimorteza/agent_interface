"""Shared logical Models of Trading Assistant.

Every Model is a validated class carrying the domain meaning that the Database,
Backend, and Frontend layers share: its fields and their properties, its
relationships, its domain rules, and its initial records. ``MODELS`` names every
Model in project order, and ``model_metadata`` returns one Model's complete
definition.

Consumers import only from this package root; no other module of the package is
part of its public interface.
"""

from ._registry import MODELS, model_metadata
from ._spec import (
    UNSET,
    FieldSpec,
    GenerateValue,
    LogicalType,
    ModelSpec,
    RelationshipSpec,
    RuleSpec,
)
from .account import Account
from .account_group import AccountGroup
from .action import Action
from .action_group import ActionGroup
from .asset import Asset
from .broker import Broker
from .currency import Currency
from .partial_group import PartialGroup
from .partial_rule import PartialRule
from .position import Position
from .trading_platform import TradingPlatform
from .trailing_group import TrailingGroup
from .trailing_rule import TrailingRule
from .user import User

__version__ = "0.1.0"

__all__ = [
    # The shared Models, in project order.
    "User",
    "Currency",
    "TradingPlatform",
    "Broker",
    "AccountGroup",
    "Account",
    "Asset",
    "TrailingGroup",
    "TrailingRule",
    "PartialGroup",
    "PartialRule",
    "ActionGroup",
    "Action",
    "Position",
    # The registry of every shared Model and the accessor for one Model's definition.
    "MODELS",
    "model_metadata",
    # The types a Model definition is made of.
    "ModelSpec",
    "FieldSpec",
    "RelationshipSpec",
    "RuleSpec",
    "LogicalType",
    "GenerateValue",
    "UNSET",
]

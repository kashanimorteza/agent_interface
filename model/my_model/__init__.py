"""my_model: the shared Model package of the Trading Assistant.

This module is the package's single public interface. Every domain Model is
exposed here exactly once under its public symbol, together with the
declaration types needed to read a Model and the validation every consumer
reuses. Consumers import from this module and never from the package's
internal modules.
"""

from .account import Account
from .account_group import AccountGroup
from .action import Action
from .action_group import ActionGroup
from .asset import Asset
from .base import (
    CredentialStorage,
    FieldSpec,
    Model,
    Pending,
    Relationship,
    Rule,
    UniqueTogether,
)
from .broker import Broker
from .currency import Currency
from .partial_group import PartialGroup
from .partial_rule import PartialRule
from .position import Position
from .trading_platform import TradingPlatform
from .trailing_group import TrailingGroup
from .trailing_rule import TrailingRule
from .user import User
from .validation import (
    Change,
    FieldError,
    InvalidValue,
    State,
    validate_change,
    validate_state,
)

#: Every domain Model, in the order the project defines them.
MODELS: tuple[type[Model], ...] = (
    User,
    Currency,
    TradingPlatform,
    Broker,
    AccountGroup,
    Account,
    Asset,
    TrailingGroup,
    TrailingRule,
    PartialGroup,
    PartialRule,
    ActionGroup,
    Action,
    Position,
)

__all__ = [
    # Domain Models
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
    "MODELS",
    # Declaration support
    "Model",
    "FieldSpec",
    "Relationship",
    "Rule",
    "UniqueTogether",
    "CredentialStorage",
    "Pending",
    # Validation
    "validate_state",
    "validate_change",
    "State",
    "Change",
    "FieldError",
    "InvalidValue",
]

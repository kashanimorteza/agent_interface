"""Model: the shared domain Model.

The one public entry point. Every Domain Definition is published here under its own name, with
the vocabulary needed to read what it declares and the Foundation types shared between them.
"""

from model.account import Account
from model.account_group import AccountGroup
from model.action import Action
from model.action_group import ActionGroup
from model.asset import Asset
from model.broker import Broker
from model.currency import Currency
from model.declaration import (
    Activation,
    AtRest,
    Cardinality,
    Credential,
    Declaration,
    FieldDeclaration,
    Generated,
    Identity,
    Persistence,
    Precision,
    Relationship,
    Unique,
)
from model.foundation import ExactDecimal, Instant, ModelFoundation
from model.instance import Instance
from model.operations import create, describe, deserialize, serialize
from model.partial_group import PartialGroup
from model.partial_rule import PartialRule
from model.position import Position
from model.trading_platform import TradingPlatform
from model.trailing_group import TrailingGroup
from model.trailing_rule import TrailingRule
from model.user import User

__all__ = [
    "Account",
    "AccountGroup",
    "Action",
    "ActionGroup",
    "Activation",
    "Asset",
    "AtRest",
    "Broker",
    "Cardinality",
    "Credential",
    "Currency",
    "Declaration",
    "ExactDecimal",
    "FieldDeclaration",
    "Generated",
    "Identity",
    "Instance",
    "Instant",
    "ModelFoundation",
    "PartialGroup",
    "PartialRule",
    "Persistence",
    "Position",
    "Precision",
    "Relationship",
    "TradingPlatform",
    "TrailingGroup",
    "TrailingRule",
    "Unique",
    "User",
    "create",
    "describe",
    "deserialize",
    "serialize",
]

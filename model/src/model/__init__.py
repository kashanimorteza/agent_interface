"""Model: the system's shared, technology-independent domain definitions.

This package is the Model Public Interface. Consumers import every Domain Definition, and the
vocabulary used to read its declaration, from here and from nowhere else::

    from model import User

Every Domain Definition offers three Operations:

* ``serialize()`` returns its Plain Representation: named values expressible in JSON.
* ``deserialize(data)`` builds a validated instance from a Plain Representation.
* ``declaration`` returns the definition in the Declaration Vocabulary.

Model stores nothing, performs no application behaviour, and offers no stored-data operations.
"""

from model.entity.account import Account
from model.entity.account_group import AccountGroup
from model.entity.action import Action
from model.entity.action_group import ActionGroup
from model.entity.asset import Asset
from model.entity.broker import Broker
from model.entity.currency import Currency
from model.entity.instance import Instance
from model.entity.partial_group import PartialGroup
from model.entity.partial_rule import PartialRule
from model.entity.position import Position
from model.entity.trading_platform import TradingPlatform
from model.entity.trailing_group import TrailingGroup
from model.entity.trailing_rule import TrailingRule
from model.entity.user import User
from model.foundation import (
    Constraint,
    Declaration,
    FieldDeclaration,
    ModelFoundation,
    Relationship,
    Rule,
    Sensitivity,
)

__all__ = [
    "Account",
    "AccountGroup",
    "Action",
    "ActionGroup",
    "Asset",
    "Broker",
    "Constraint",
    "Currency",
    "Declaration",
    "FieldDeclaration",
    "Instance",
    "ModelFoundation",
    "PartialGroup",
    "PartialRule",
    "Position",
    "Relationship",
    "Rule",
    "Sensitivity",
    "TradingPlatform",
    "TrailingGroup",
    "TrailingRule",
    "User",
]

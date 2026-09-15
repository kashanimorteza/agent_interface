"""Verifies the Model package's Public Interface and serialization/schema generation."""

import model
from model import (
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
)

ALL_DOMAIN_DEFINITIONS = [
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
]


def test_every_domain_definition_is_publicly_reachable() -> None:
    assert set(model.__all__) == {cls.__name__ for cls in ALL_DOMAIN_DEFINITIONS}
    by_name = {cls.__name__: cls for cls in ALL_DOMAIN_DEFINITIONS}
    for name in model.__all__:
        assert getattr(model, name) is by_name[name]


def test_every_domain_definition_serializes_and_generates_a_schema() -> None:
    for cls in ALL_DOMAIN_DEFINITIONS:
        schema = cls.model_json_schema()
        assert isinstance(schema, dict)
        assert schema.get("title") == cls.__name__

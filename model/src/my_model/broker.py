"""The Broker Model."""

from collections.abc import Mapping
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, LogicalType, RelationshipSpec, RuleSpec


class Broker(Model):
    """Defines a broker that the system can work with through its selected trading platform. Multiple
    brokers can be added so the system is not limited to a specific broker and can operate with any
    configured broker.
    """

    logical_key: ClassVar[str] = "broker"
    logical_purpose: ClassVar[str] = (
        "Defines a broker that the system can work with through its selected trading platform. Multiple "
        "brokers can be added so the system is not limited to a specific broker and can operate with any "
        "configured broker."
    )
    logical_relationships: ClassVar[tuple[RelationshipSpec, ...]] = (
        RelationshipSpec(name="user", type="belongs_to", target="user", field="user_id"),
        RelationshipSpec(
            name="trading_platform",
            type="belongs_to",
            target="trading_platform",
            field="trading_platform_id",
        ),
    )
    logical_rules: ClassVar[tuple[RuleSpec, ...]] = (
        RuleSpec(
            rule="The combination of user_id and name must be unique.",
            kind="unique",
            fields=("user_id", "name"),
        ),
    )
    logical_initial_data: ClassVar[tuple[Mapping[str, object], ...]] = (
        {"name": "FxPro", "user_id": 1, "trading_platform_id": 1},
    )

    id: Annotated[
        int | None,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            auto_increment=True,
            primary_key=True,
        ),
    ] = None
    name: Annotated[str, FieldSpec(type=LogicalType.string, nullable=False, purpose="The broker's display name.")]
    user_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the user who owns the broker configuration.",
        ),
    ]
    trading_platform_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the trading platform used by the broker.",
        ),
    ]
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the broker is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the broker.",
        ),
    ] = None

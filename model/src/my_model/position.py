"""The Position Model."""

from decimal import Decimal
from datetime import datetime
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, LogicalType, RelationshipSpec


class Position(Model):
    """Stores the complete information for every position created by the system. It allows the system
    to identify and track positions that have been opened as well as positions that are still
    pending execution.
    """

    logical_key: ClassVar[str] = "position"
    logical_purpose: ClassVar[str] = (
        "Stores the complete information for every position created by the system. It allows the system to "
        "identify and track positions that have been opened as well as positions that are still pending "
        "execution."
    )
    logical_relationships: ClassVar[tuple[RelationshipSpec, ...]] = (
        RelationshipSpec(
            name="trading_platform",
            type="uses",
            target="trading_platform",
            field="trading_platform_id",
        ),
        RelationshipSpec(name="broker", type="uses", target="broker", field="broker_id"),
        RelationshipSpec(name="account", type="uses", target="account", field="account_id"),
        RelationshipSpec(name="trailing_group", type="uses", target="trailing_group", field="trailing_group_id"),
        RelationshipSpec(name="partial_group", type="uses", target="partial_group", field="partial_group_id"),
        RelationshipSpec(name="action_group", type="uses", target="action_group", field="action_group_id"),
        RelationshipSpec(name="action", type="belongs_to", target="action", field="action_id"),
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
    name: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            unique=True,
            purpose="The position's display name.",
        ),
    ]
    trading_platform_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the trading platform used to execute the position.",
        ),
    ]
    broker_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the broker through which the position is executed.",
        ),
    ]
    account_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the trading account used for the position.",
        ),
    ]
    trailing_group_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the Trailing Group applied to the position.",
        ),
    ]
    partial_group_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the Partial Group applied to the position.",
        ),
    ]
    action_group_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the Action Group associated with the position.",
        ),
    ]
    action_id: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            purpose="Identifies the action from which the position is created.",
        ),
    ]
    date: Annotated[
        datetime,
        FieldSpec(
            type=LogicalType.datetime,
            nullable=False,
            purpose="Stores the position's date and time.",
        ),
    ]
    volume: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            purpose="Stores the position's trading volume.",
        ),
    ]
    profit: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            default=0,
            purpose="Stores the position's current profit or loss.",
        ),
    ] = Decimal("0")
    is_executed: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=False,
            purpose="Indicates whether the position has been executed.",
        ),
    ] = False
    order_type: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            purpose="Stores the position's order type.",
        ),
    ]
    base_tp: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            purpose="Stores the position's initial Take Profit value.",
        ),
    ]
    base_sl: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            purpose="Stores the position's initial Stop Loss value.",
        ),
    ]
    real_tp: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            purpose="Stores the position's current Take Profit value.",
        ),
    ]
    real_sl: Annotated[
        Decimal,
        FieldSpec(
            type=LogicalType.decimal,
            nullable=False,
            purpose="Stores the position's current Stop Loss value.",
        ),
    ]
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the position is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the position.",
        ),
    ] = None

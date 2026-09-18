"""The Position Domain Definition: the complete information for every position created by the system, opened or still pending execution."""

from __future__ import annotations

from decimal import Decimal

from pydantic import AwareDatetime

from model.foundation import DomainModel, ForeignKeyDeclaration, domain_field


class Position(DomainModel):
    persistent = True

    id: int | None = domain_field(
        type="integer", nullable=False, primary_key=True, auto_increment=True
    )
    user_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="User", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the user who owns the position.",
    )
    name: str = domain_field(
        type="string",
        nullable=False,
        unique=True,
        description="The position's display name.",
    )
    trading_platform_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="TradingPlatform",
            field="id",
            cardinality="many_to_one",
            optional=False,
        ),
        description="Identifies the trading platform used to execute the position.",
    )
    broker_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="Broker", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the broker through which the position is executed.",
    )
    account_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="Account", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the trading account used for the position.",
    )
    trailing_group_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="TrailingGroup",
            field="id",
            cardinality="many_to_one",
            optional=False,
        ),
        description="Identifies the Trailing Group applied to the position.",
    )
    partial_group_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="PartialGroup",
            field="id",
            cardinality="many_to_one",
            optional=False,
        ),
        description="Identifies the Partial Group applied to the position.",
    )
    action_group_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="ActionGroup",
            field="id",
            cardinality="many_to_one",
            optional=False,
        ),
        description="Identifies the Action Group associated with the position.",
    )
    action_id: int = domain_field(
        type="integer",
        nullable=False,
        foreign_key=ForeignKeyDeclaration(
            references="Action", field="id", cardinality="many_to_one", optional=False
        ),
        description="Identifies the action from which the position is created.",
    )
    date: AwareDatetime = domain_field(
        type="datetime",
        nullable=False,
        description="Stores the position's date and time.",
    )
    volume: Decimal = domain_field(
        type="decimal",
        nullable=False,
        description="Stores the position's trading volume.",
    )
    profit: Decimal = domain_field(
        type="decimal",
        nullable=False,
        default=Decimal(0),
        description="Stores the position's current profit or loss.",
    )
    is_executed: bool = domain_field(
        type="boolean",
        nullable=False,
        default=False,
        description="Indicates whether the position has been executed.",
    )
    order_type: str = domain_field(
        type="string", nullable=False, description="Stores the position's order type."
    )
    base_tp: Decimal = domain_field(
        type="decimal",
        nullable=False,
        description="Stores the position's initial Take Profit value.",
    )
    base_sl: Decimal = domain_field(
        type="decimal",
        nullable=False,
        description="Stores the position's initial Stop Loss value.",
    )
    real_tp: Decimal = domain_field(
        type="decimal",
        nullable=False,
        description="Stores the position's current Take Profit value.",
    )
    real_sl: Decimal = domain_field(
        type="decimal",
        nullable=False,
        description="Stores the position's current Stop Loss value.",
    )
    is_active: bool = domain_field(
        type="boolean",
        nullable=False,
        default=True,
        description="Indicates whether the position is active.",
    )
    description: str | None = domain_field(
        type="string", nullable=True, description="Describes the position."
    )

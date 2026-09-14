from datetime import datetime
from decimal import Decimal

from model import Action, ActionGroup, Position
from sqlalchemy import Boolean, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..foundation import StorageBase, UTCDateTime
from . import register


@register(ActionGroup)
class ActionGroupRow(StorageBase):
    __tablename__ = "action_groups"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_action_groups_user_id_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(nullable=True)


@register(Action)
class ActionRow(StorageBase):
    __tablename__ = "actions"
    __table_args__ = (
        UniqueConstraint(
            "action_group_id", "name", name="uq_actions_action_group_id_name"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    action_group_id: Mapped[int] = mapped_column(
        ForeignKey("action_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    risk_by_reward: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    take_profit: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    stop_loss: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(nullable=True)


@register(Position)
class PositionRow(StorageBase):
    __tablename__ = "positions"
    __table_args__ = (UniqueConstraint("name", name="uq_positions_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(nullable=False)
    trading_platform_id: Mapped[int] = mapped_column(
        ForeignKey("trading_platforms.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    broker_id: Mapped[int] = mapped_column(
        ForeignKey("brokers.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    action_group_id: Mapped[int] = mapped_column(
        ForeignKey("action_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    action_id: Mapped[int] = mapped_column(
        ForeignKey("actions.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    date: Mapped[datetime] = mapped_column(UTCDateTime, nullable=False)
    volume: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    profit: Mapped[Decimal] = mapped_column(Numeric, nullable=False, default=Decimal(0))
    is_executed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    order_type: Mapped[str] = mapped_column(nullable=False)
    base_tp: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    base_sl: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    real_tp: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    real_sl: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

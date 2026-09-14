"""Storage mappings for Action Group, Action, and Position."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, UTCDateTime


class ActionGroupTable(Base):
    __tablename__ = "action_groups"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_action_groups_user_id_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class ActionTable(Base):
    __tablename__ = "actions"
    __table_args__ = (UniqueConstraint("action_group_id", "name", name="uq_actions_group_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    action_group_id: Mapped[int] = mapped_column(
        ForeignKey("action_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    risk_by_reward: Mapped[Decimal] = mapped_column(Numeric(9, 4), nullable=False)
    take_profit: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    stop_loss: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class PositionTable(Base):
    __tablename__ = "positions"
    __table_args__ = (UniqueConstraint("name", name="uq_positions_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    trading_platform_id: Mapped[int] = mapped_column(
        ForeignKey("trading_platforms.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    broker_id: Mapped[int] = mapped_column(
        ForeignKey("brokers.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    action_group_id: Mapped[int] = mapped_column(
        ForeignKey("action_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    action_id: Mapped[int] = mapped_column(
        ForeignKey("actions.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    date: Mapped[UTCDateTime] = mapped_column(UTCDateTime, nullable=False)
    volume: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    profit: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False, default=Decimal("0"))
    is_executed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    order_type: Mapped[str] = mapped_column(String, nullable=False)
    base_tp: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    base_sl: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    real_tp: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    real_sl: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

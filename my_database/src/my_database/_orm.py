"""Data Logic and Mapping: persistence mapping of every domain entity.

Persistence-only classes. Domain meaning, fields, relationships, and rules
are resolved from the Model package; this module only derives their storage
representation (tables, columns, foreign keys, unique constraints).
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from my_database._base import Base


class UserRow(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("name", name="uq_users_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    api_key: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class TradingPlatformRow(Base):
    __tablename__ = "trading_platforms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class CurrencyRow(Base):
    __tablename__ = "currencies"
    __table_args__ = (
        UniqueConstraint("user_id", "code", name="uq_currencies_user_id_code"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(3), nullable=False)
    symbol: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    decimal_digits: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class BrokerRow(Base):
    __tablename__ = "brokers"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_brokers_user_id_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class InstanceRow(Base):
    __tablename__ = "instances"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_instances_user_id_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    trading_platform_id: Mapped[int] = mapped_column(
        ForeignKey("trading_platforms.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    ip: Mapped[str | None] = mapped_column(String, nullable=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    password: Mapped[str | None] = mapped_column(String, nullable=True)
    api_key: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class AssetRow(Base):
    __tablename__ = "assets"
    __table_args__ = (
        UniqueConstraint("broker_id", "symbol", name="uq_assets_broker_id_symbol"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    broker_id: Mapped[int] = mapped_column(
        ForeignKey("brokers.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    point_size: Mapped[float] = mapped_column(
        Numeric(asdecimal=False), nullable=False, default=0.0
    )
    digits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class AccountGroupRow(Base):
    __tablename__ = "account_groups"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_account_groups_user_id_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class AccountRow(Base):
    __tablename__ = "accounts"
    __table_args__ = (
        UniqueConstraint("name", name="uq_accounts_name"),
        UniqueConstraint(
            "group_id",
            "broker_id",
            "instance_id",
            name="uq_accounts_group_id_broker_id_instance_id",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("account_groups.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    broker_id: Mapped[int] = mapped_column(
        ForeignKey("brokers.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    instance_id: Mapped[int] = mapped_column(
        ForeignKey("instances.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    base_currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    leverage: Mapped[int] = mapped_column(Integer, nullable=False)
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=18, scale=4), nullable=False, default=Decimal(0)
    )
    account_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class TrailingGroupRow(Base):
    __tablename__ = "trailing_groups"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_trailing_groups_user_id_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class TrailingRuleRow(Base):
    __tablename__ = "trailing_rules"
    __table_args__ = (
        UniqueConstraint("name", name="uq_trailing_rules_name"),
        UniqueConstraint(
            "trailing_group_id",
            "trigger_percentage",
            name="uq_trailing_rules_group_id_trigger_percentage",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    trigger_percentage: Mapped[Decimal] = mapped_column(
        Numeric(precision=9, scale=4), nullable=False
    )
    take_profit_adjustment: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=18, scale=6), nullable=True
    )
    stop_loss_adjustment: Mapped[Decimal | None] = mapped_column(
        Numeric(precision=18, scale=6), nullable=True
    )
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class PartialGroupRow(Base):
    __tablename__ = "partial_groups"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_partial_groups_user_id_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class PartialRuleRow(Base):
    __tablename__ = "partial_rules"
    __table_args__ = (
        UniqueConstraint("name", name="uq_partial_rules_name"),
        UniqueConstraint(
            "partial_group_id",
            "profit_percentage",
            name="uq_partial_rules_group_id_profit_percentage",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    profit_percentage: Mapped[Decimal] = mapped_column(
        Numeric(precision=9, scale=4), nullable=False
    )
    close_percentage: Mapped[Decimal] = mapped_column(
        Numeric(precision=9, scale=4), nullable=False
    )
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class ActionGroupRow(Base):
    __tablename__ = "action_groups"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_action_groups_user_id_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class ActionRow(Base):
    __tablename__ = "actions"
    __table_args__ = (
        UniqueConstraint(
            "action_group_id", "name", name="uq_actions_action_group_id_name"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    action_group_id: Mapped[int] = mapped_column(
        ForeignKey("action_groups.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    risk_by_reward: Mapped[Decimal] = mapped_column(
        Numeric(precision=9, scale=4), nullable=False
    )
    take_profit: Mapped[Decimal] = mapped_column(
        Numeric(precision=18, scale=6), nullable=False
    )
    stop_loss: Mapped[Decimal] = mapped_column(
        Numeric(precision=18, scale=6), nullable=False
    )
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class PositionRow(Base):
    __tablename__ = "positions"
    __table_args__ = (UniqueConstraint("name", name="uq_positions_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    trading_platform_id: Mapped[int] = mapped_column(
        ForeignKey("trading_platforms.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    broker_id: Mapped[int] = mapped_column(
        ForeignKey("brokers.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    action_group_id: Mapped[int] = mapped_column(
        ForeignKey("action_groups.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    action_id: Mapped[int] = mapped_column(
        ForeignKey("actions.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    volume: Mapped[Decimal] = mapped_column(
        Numeric(precision=18, scale=6), nullable=False
    )
    profit: Mapped[Decimal] = mapped_column(
        Numeric(precision=18, scale=6), nullable=False, default=Decimal(0)
    )
    is_executed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    order_type: Mapped[str] = mapped_column(String, nullable=False)
    base_tp: Mapped[Decimal] = mapped_column(
        Numeric(precision=18, scale=6), nullable=False
    )
    base_sl: Mapped[Decimal] = mapped_column(
        Numeric(precision=18, scale=6), nullable=False
    )
    real_tp: Mapped[Decimal] = mapped_column(
        Numeric(precision=18, scale=6), nullable=False
    )
    real_sl: Mapped[Decimal] = mapped_column(
        Numeric(precision=18, scale=6), nullable=False
    )
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

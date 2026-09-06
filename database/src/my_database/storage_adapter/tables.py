"""Mapped tables — the storage schema exactly as resolved in .interface/config/database.yaml."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from my_database.storage_adapter.base import Base, decimal_type

TRUE, FALSE = text("1"), text("0")


def _fk(target: str) -> ForeignKey:
    """A foreign key with the resolved referential actions."""
    return ForeignKey(target, ondelete="RESTRICT", onupdate="RESTRICT")


# ---------------------------------------------------------------- independent tables


class User(Base):
    __tablename__ = "users"
    __model_key__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    api_key: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class Currency(Base):
    __tablename__ = "currencies"
    __model_key__ = "currency"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String(3), nullable=False, unique=True)
    symbol: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    decimal_digits: Mapped[int] = mapped_column(Integer, nullable=False, default=2, server_default=text("2"))
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class TradingPlatform(Base):
    __tablename__ = "trading_platforms"
    __model_key__ = "trading_platform"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class Asset(Base):
    __tablename__ = "assets"
    __model_key__ = "asset"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    category: Mapped[str] = mapped_column(String, nullable=False)
    point_size: Mapped[float] = mapped_column(Float, nullable=False, default=0.0, server_default=text("0.0"))
    digits: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default=text("0"))
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class TrailingGroup(Base):
    __tablename__ = "trailing_groups"
    __model_key__ = "trailing_group"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class PartialGroup(Base):
    __tablename__ = "partial_groups"
    __model_key__ = "partial_group"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class ActionGroup(Base):
    __tablename__ = "action_groups"
    __model_key__ = "action_group"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


# ---------------------------------------------------------------- first-level dependent tables


class Broker(Base):
    __tablename__ = "brokers"
    __model_key__ = "broker"
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, _fk("users.id"), nullable=False, index=True)
    trading_platform_id: Mapped[int] = mapped_column(Integer, _fk("trading_platforms.id"), nullable=False, index=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class Account(Base):
    __tablename__ = "accounts"
    __model_key__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    broker_id: Mapped[int] = mapped_column(Integer, _fk("brokers.id"), nullable=False, index=True)
    base_currency_id: Mapped[int] = mapped_column(Integer, _fk("currencies.id"), nullable=False, index=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    leverage: Mapped[int] = mapped_column(Integer, nullable=False)
    balance = mapped_column(decimal_type(), nullable=False, default=0, server_default=text("0"))
    account_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class TrailingRule(Base):
    __tablename__ = "trailing_rules"
    __model_key__ = "trailing_rule"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    trailing_group_id: Mapped[int] = mapped_column(Integer, _fk("trailing_groups.id"), nullable=False, index=True)
    trigger_percentage = mapped_column(decimal_type(), nullable=False)
    take_profit_adjustment = mapped_column(decimal_type(), nullable=True)
    stop_loss_adjustment = mapped_column(decimal_type(), nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class PartialRule(Base):
    __tablename__ = "partial_rules"
    __model_key__ = "partial_rule"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    partial_group_id: Mapped[int] = mapped_column(Integer, _fk("partial_groups.id"), nullable=False, index=True)
    profit_percentage = mapped_column(decimal_type(), nullable=False)
    close_percentage = mapped_column(decimal_type(), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


# ---------------------------------------------------------------- actions and positions


class Action(Base):
    __tablename__ = "actions"
    __model_key__ = "action"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    action_group_id: Mapped[int] = mapped_column(Integer, _fk("action_groups.id"), nullable=False, index=True)
    asset_id: Mapped[int] = mapped_column(Integer, _fk("assets.id"), nullable=False, index=True)
    account_id: Mapped[int] = mapped_column(Integer, _fk("accounts.id"), nullable=False, index=True)
    partial_group_id: Mapped[int] = mapped_column(Integer, _fk("partial_groups.id"), nullable=False, index=True)
    trailing_group_id: Mapped[int] = mapped_column(Integer, _fk("trailing_groups.id"), nullable=False, index=True)
    risk_by_reward = mapped_column(decimal_type(), nullable=False)
    take_profit = mapped_column(decimal_type(), nullable=False)
    stop_loss = mapped_column(decimal_type(), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class Position(Base):
    __tablename__ = "positions"
    __model_key__ = "position"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    trading_platform_id: Mapped[int] = mapped_column(Integer, _fk("trading_platforms.id"), nullable=False, index=True)
    broker_id: Mapped[int] = mapped_column(Integer, _fk("brokers.id"), nullable=False, index=True)
    account_id: Mapped[int] = mapped_column(Integer, _fk("accounts.id"), nullable=False, index=True)
    trailing_group_id: Mapped[int] = mapped_column(Integer, _fk("trailing_groups.id"), nullable=False, index=True)
    partial_group_id: Mapped[int] = mapped_column(Integer, _fk("partial_groups.id"), nullable=False, index=True)
    action_group_id: Mapped[int] = mapped_column(Integer, _fk("action_groups.id"), nullable=False, index=True)
    action_id: Mapped[int] = mapped_column(Integer, _fk("actions.id"), nullable=False, index=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    volume = mapped_column(decimal_type(), nullable=False)
    profit = mapped_column(decimal_type(), nullable=False, default=0, server_default=text("0"))
    is_executed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=FALSE)
    order_type: Mapped[str] = mapped_column(String, nullable=False)
    base_tp = mapped_column(decimal_type(), nullable=False)
    base_sl = mapped_column(decimal_type(), nullable=False)
    real_tp = mapped_column(decimal_type(), nullable=False)
    real_sl = mapped_column(decimal_type(), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=TRUE)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

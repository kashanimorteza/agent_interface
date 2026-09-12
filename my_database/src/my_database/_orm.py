"""Storage mapping: every persistent domain entity mapped to its table.

Column types, nullability, and foreign keys trace back to the current
``my_model`` definitions (Task P2-T2). Every uniqueness rule the Target
declares for an entity is reproduced here as a storage-level
:class:`~sqlalchemy.UniqueConstraint`, since Model itself cannot enforce a
rule that depends on other stored rows (Model Standard 13; Database Standard
2.10). Financial and percentage values use a portable fixed-precision
``Numeric(18, 6)`` regardless of the selected Engine.
"""

from __future__ import annotations

from datetime import datetime

import my_model as m
from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DECIMAL = Numeric(18, 6)


class Base(DeclarativeBase):
    pass


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


class InstanceRow(Base):
    __tablename__ = "instances"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_instances_user_id_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    trading_platform_id: Mapped[int] = mapped_column(
        ForeignKey("trading_platforms.id"), nullable=False, index=True
    )
    ip: Mapped[str | None] = mapped_column(String, nullable=True)
    username: Mapped[str | None] = mapped_column(String, nullable=True)
    password: Mapped[str | None] = mapped_column(String, nullable=True)
    api_key: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class CurrencyRow(Base):
    __tablename__ = "currencies"
    __table_args__ = (UniqueConstraint("user_id", "code", name="uq_currencies_user_id_code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    code: Mapped[str] = mapped_column(String, nullable=False)
    symbol: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    decimal_digits: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class BrokerRow(Base):
    __tablename__ = "brokers"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_brokers_user_id_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class AssetRow(Base):
    __tablename__ = "assets"
    __table_args__ = (UniqueConstraint("broker_id", "symbol", name="uq_assets_broker_id_symbol"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    broker_id: Mapped[int] = mapped_column(ForeignKey("brokers.id"), nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    point_size: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    digits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class AccountGroupRow(Base):
    __tablename__ = "account_groups"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_account_groups_user_id_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class AccountRow(Base):
    __tablename__ = "accounts"
    __table_args__ = (
        UniqueConstraint("name", name="uq_accounts_name"),
        UniqueConstraint(
            "group_id", "broker_id", "instance_id", name="uq_accounts_group_broker_instance"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("account_groups.id"), nullable=False, index=True
    )
    broker_id: Mapped[int] = mapped_column(ForeignKey("brokers.id"), nullable=False, index=True)
    instance_id: Mapped[int] = mapped_column(ForeignKey("instances.id"), nullable=False, index=True)
    base_currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"), nullable=False, index=True
    )
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    leverage: Mapped[int] = mapped_column(Integer, nullable=False)
    balance: Mapped[object] = mapped_column(DECIMAL, nullable=False, default=0)
    account_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class TrailingGroupRow(Base):
    __tablename__ = "trailing_groups"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_trailing_groups_user_id_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class TrailingRuleRow(Base):
    __tablename__ = "trailing_rules"
    __table_args__ = (
        UniqueConstraint("name", name="uq_trailing_rules_name"),
        UniqueConstraint(
            "trailing_group_id", "trigger_percentage", name="uq_trailing_rules_group_trigger"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id"), nullable=False, index=True
    )
    trigger_percentage: Mapped[object] = mapped_column(DECIMAL, nullable=False)
    take_profit_adjustment: Mapped[object | None] = mapped_column(DECIMAL, nullable=True)
    stop_loss_adjustment: Mapped[object | None] = mapped_column(DECIMAL, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class PartialGroupRow(Base):
    __tablename__ = "partial_groups"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_partial_groups_user_id_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class PartialRuleRow(Base):
    __tablename__ = "partial_rules"
    __table_args__ = (
        UniqueConstraint("name", name="uq_partial_rules_name"),
        UniqueConstraint(
            "partial_group_id", "profit_percentage", name="uq_partial_rules_group_profit"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id"), nullable=False, index=True
    )
    profit_percentage: Mapped[object] = mapped_column(DECIMAL, nullable=False)
    close_percentage: Mapped[object] = mapped_column(DECIMAL, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class ActionGroupRow(Base):
    __tablename__ = "action_groups"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_action_groups_user_id_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class ActionRow(Base):
    __tablename__ = "actions"
    __table_args__ = (UniqueConstraint("action_group_id", "name", name="uq_actions_group_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    action_group_id: Mapped[int] = mapped_column(
        ForeignKey("action_groups.id"), nullable=False, index=True
    )
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False, index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False, index=True)
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id"), nullable=False, index=True
    )
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id"), nullable=False, index=True
    )
    risk_by_reward: Mapped[object] = mapped_column(DECIMAL, nullable=False)
    take_profit: Mapped[object] = mapped_column(DECIMAL, nullable=False)
    stop_loss: Mapped[object] = mapped_column(DECIMAL, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class PositionRow(Base):
    __tablename__ = "positions"
    __table_args__ = (UniqueConstraint("name", name="uq_positions_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    trading_platform_id: Mapped[int] = mapped_column(
        ForeignKey("trading_platforms.id"), nullable=False, index=True
    )
    broker_id: Mapped[int] = mapped_column(ForeignKey("brokers.id"), nullable=False, index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False, index=True)
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id"), nullable=False, index=True
    )
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id"), nullable=False, index=True
    )
    action_group_id: Mapped[int] = mapped_column(
        ForeignKey("action_groups.id"), nullable=False, index=True
    )
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.id"), nullable=False, index=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    volume: Mapped[object] = mapped_column(DECIMAL, nullable=False)
    profit: Mapped[object] = mapped_column(DECIMAL, nullable=False, default=0)
    is_executed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    order_type: Mapped[str] = mapped_column(String, nullable=False)
    base_tp: Mapped[object] = mapped_column(DECIMAL, nullable=False)
    base_sl: Mapped[object] = mapped_column(DECIMAL, nullable=False)
    real_tp: Mapped[object] = mapped_column(DECIMAL, nullable=False)
    real_sl: Mapped[object] = mapped_column(DECIMAL, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


#: Maps every persistent my_model type to its mapped storage row class.
MODEL_TO_ROW: dict[type[m.BaseModel], type[Base]] = {
    m.User: UserRow,
    m.TradingPlatform: TradingPlatformRow,
    m.Instance: InstanceRow,
    m.Currency: CurrencyRow,
    m.Broker: BrokerRow,
    m.Asset: AssetRow,
    m.AccountGroup: AccountGroupRow,
    m.Account: AccountRow,
    m.TrailingGroup: TrailingGroupRow,
    m.TrailingRule: TrailingRuleRow,
    m.PartialGroup: PartialGroupRow,
    m.PartialRule: PartialRuleRow,
    m.ActionGroup: ActionGroupRow,
    m.Action: ActionRow,
    m.Position: PositionRow,
}

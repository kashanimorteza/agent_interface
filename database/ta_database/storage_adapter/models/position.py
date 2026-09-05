from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, UniqueConstraint, false, true
from sqlalchemy.orm import Mapped, mapped_column

from ta_database.storage_adapter.base import Base


class Position(Base):
    __tablename__ = "positions"
    __table_args__ = (
        UniqueConstraint("name", name="uq_positions_name"),
        Index("ix_positions_trading_platform_id", "trading_platform_id"),
        Index("ix_positions_broker_id", "broker_id"),
        Index("ix_positions_account_id", "account_id"),
        Index("ix_positions_trailing_group_id", "trailing_group_id"),
        Index("ix_positions_partial_group_id", "partial_group_id"),
        Index("ix_positions_action_group_id", "action_group_id"),
        Index("ix_positions_action_id", "action_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    trading_platform_id: Mapped[int] = mapped_column(Integer, ForeignKey("trading_platforms.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    broker_id: Mapped[int] = mapped_column(Integer, ForeignKey("brokers.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    trailing_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("trailing_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    partial_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("partial_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    action_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("action_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    action_id: Mapped[int] = mapped_column(Integer, ForeignKey("actions.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    volume: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    profit: Mapped[Decimal] = mapped_column(Numeric, nullable=False, default=0, server_default="0")
    is_executed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=false())
    order_type: Mapped[str] = mapped_column(String, nullable=False)
    base_tp: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    base_sl: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    real_tp: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    real_sl: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=true())
    description: Mapped[str | None] = mapped_column(String, nullable=True)

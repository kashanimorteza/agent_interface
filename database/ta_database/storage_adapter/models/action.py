from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Index, Integer, Numeric, String, UniqueConstraint, true
from sqlalchemy.orm import Mapped, mapped_column

from ta_database.storage_adapter.base import Base


class Action(Base):
    __tablename__ = "actions"
    __table_args__ = (
        UniqueConstraint("name", name="uq_actions_name"),
        Index("ix_actions_action_group_id", "action_group_id"),
        Index("ix_actions_asset_id", "asset_id"),
        Index("ix_actions_account_id", "account_id"),
        Index("ix_actions_partial_group_id", "partial_group_id"),
        Index("ix_actions_trailing_group_id", "trailing_group_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    action_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("action_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    asset_id: Mapped[int] = mapped_column(Integer, ForeignKey("assets.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    partial_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("partial_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    trailing_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("trailing_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    risk_by_reward: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    take_profit: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    stop_loss: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=true())
    description: Mapped[str | None] = mapped_column(String, nullable=True)

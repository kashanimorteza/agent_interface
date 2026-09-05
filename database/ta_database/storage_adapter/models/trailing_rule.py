from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Index, Integer, Numeric, String, UniqueConstraint, true
from sqlalchemy.orm import Mapped, mapped_column

from ta_database.storage_adapter.base import Base


class TrailingRule(Base):
    __tablename__ = "trailing_rules"
    __table_args__ = (
        UniqueConstraint("name", name="uq_trailing_rules_name"),
        Index("ix_trailing_rules_trailing_group_id", "trailing_group_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    trailing_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("trailing_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    trigger_percentage: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    take_profit_adjustment: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    stop_loss_adjustment: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=true())
    description: Mapped[str | None] = mapped_column(String, nullable=True)

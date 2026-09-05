from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Index, Integer, Numeric, String, UniqueConstraint, true
from sqlalchemy.orm import Mapped, mapped_column

from ta_database.storage_adapter.base import Base


class PartialRule(Base):
    __tablename__ = "partial_rules"
    __table_args__ = (
        UniqueConstraint("name", name="uq_partial_rules_name"),
        Index("ix_partial_rules_partial_group_id", "partial_group_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    partial_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("partial_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    profit_percentage: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    close_percentage: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=true())
    description: Mapped[str | None] = mapped_column(String, nullable=True)

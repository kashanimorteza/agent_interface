"""Storage mappings for Trailing Group, Trailing Rule, Partial Group, and Partial Rule."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TrailingGroupTable(Base):
    __tablename__ = "trailing_groups"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_trailing_groups_user_id_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class TrailingRuleTable(Base):
    __tablename__ = "trailing_rules"
    __table_args__ = (
        UniqueConstraint("name", name="uq_trailing_rules_name"),
        UniqueConstraint(
            "trailing_group_id",
            "trigger_percentage",
            name="uq_trailing_rules_group_trigger",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    trigger_percentage: Mapped[Decimal] = mapped_column(Numeric(9, 4), nullable=False)
    take_profit_adjustment: Mapped[Decimal | None] = mapped_column(Numeric(18, 8), nullable=True)
    stop_loss_adjustment: Mapped[Decimal | None] = mapped_column(Numeric(18, 8), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class PartialGroupTable(Base):
    __tablename__ = "partial_groups"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_partial_groups_user_id_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class PartialRuleTable(Base):
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
        ForeignKey("partial_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    profit_percentage: Mapped[Decimal] = mapped_column(Numeric(9, 4), nullable=False)
    close_percentage: Mapped[Decimal] = mapped_column(Numeric(9, 4), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

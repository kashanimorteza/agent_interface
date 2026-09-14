from decimal import Decimal

from model import PartialGroup, PartialRule, TrailingGroup, TrailingRule
from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..foundation import StorageBase
from . import register


@register(TrailingGroup)
class TrailingGroupRow(StorageBase):
    __tablename__ = "trailing_groups"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_trailing_groups_user_id_name"),
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


@register(TrailingRule)
class TrailingRuleRow(StorageBase):
    __tablename__ = "trailing_rules"
    __table_args__ = (
        UniqueConstraint("name", name="uq_trailing_rules_name"),
        UniqueConstraint(
            "trailing_group_id",
            "trigger_percentage",
            name="uq_trailing_rules_trailing_group_id_trigger_percentage",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    trigger_percentage: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    take_profit_adjustment: Mapped[Decimal | None] = mapped_column(
        Numeric, nullable=True
    )
    stop_loss_adjustment: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(nullable=True)


@register(PartialGroup)
class PartialGroupRow(StorageBase):
    __tablename__ = "partial_groups"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_partial_groups_user_id_name"),
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


@register(PartialRule)
class PartialRuleRow(StorageBase):
    __tablename__ = "partial_rules"
    __table_args__ = (
        UniqueConstraint("name", name="uq_partial_rules_name"),
        UniqueConstraint(
            "partial_group_id",
            "profit_percentage",
            name="uq_partial_rules_partial_group_id_profit_percentage",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    profit_percentage: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    close_percentage: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

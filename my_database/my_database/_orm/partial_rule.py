from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from my_database._orm._base import Base


class PartialRuleRow(Base):
    __tablename__ = "partial_rules"
    __table_args__ = (
        UniqueConstraint("name", name="uq_partial_rules_name"),
        UniqueConstraint(
            "partial_group_id", "profit_percentage", name="uq_partial_rules_group_profit"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    profit_percentage: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    close_percentage: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    status: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(default=None)

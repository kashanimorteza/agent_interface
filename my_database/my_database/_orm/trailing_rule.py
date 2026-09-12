from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from my_database._orm._base import Base


class TrailingRuleRow(Base):
    __tablename__ = "trailing_rules"
    __table_args__ = (
        UniqueConstraint("name", name="uq_trailing_rules_name"),
        UniqueConstraint(
            "trailing_group_id", "trigger_percentage", name="uq_trailing_rules_group_trigger"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    trigger_percentage: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    take_profit_adjustment: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), default=None)
    stop_loss_adjustment: Mapped[Decimal | None] = mapped_column(Numeric(18, 6), default=None)
    status: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(default=None)

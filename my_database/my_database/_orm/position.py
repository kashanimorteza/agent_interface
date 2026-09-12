from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from my_database._orm._base import Base


class PositionRow(Base):
    __tablename__ = "positions"
    __table_args__ = (UniqueConstraint("name", name="uq_positions_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    name: Mapped[str]
    trading_platform_id: Mapped[int] = mapped_column(
        ForeignKey("trading_platforms.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    broker_id: Mapped[int] = mapped_column(
        ForeignKey("brokers.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    action_group_id: Mapped[int] = mapped_column(
        ForeignKey("action_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    action_id: Mapped[int] = mapped_column(
        ForeignKey("actions.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    date: Mapped[datetime]
    volume: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    profit: Mapped[Decimal] = mapped_column(Numeric(18, 6), default=Decimal(0))
    is_executed: Mapped[bool] = mapped_column(default=False)
    order_type: Mapped[str]
    base_tp: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    base_sl: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    real_tp: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    real_sl: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    status: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(default=None)

from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from my_database._orm._base import Base


class ActionRow(Base):
    __tablename__ = "actions"
    __table_args__ = (
        UniqueConstraint("action_group_id", "name", name="uq_actions_action_group_id_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    action_group_id: Mapped[int] = mapped_column(
        ForeignKey("action_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("assets.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    partial_group_id: Mapped[int] = mapped_column(
        ForeignKey("partial_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    trailing_group_id: Mapped[int] = mapped_column(
        ForeignKey("trailing_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    risk_by_reward: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    take_profit: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    stop_loss: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    status: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(default=None)

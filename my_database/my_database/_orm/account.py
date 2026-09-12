from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from my_database._orm._base import Base


class AccountRow(Base):
    __tablename__ = "accounts"
    __table_args__ = (
        UniqueConstraint("name", name="uq_accounts_name"),
        UniqueConstraint(
            "group_id", "broker_id", "instance_id", name="uq_accounts_group_broker_instance"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    group_id: Mapped[int] = mapped_column(
        ForeignKey("account_groups.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    broker_id: Mapped[int] = mapped_column(
        ForeignKey("brokers.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    instance_id: Mapped[int] = mapped_column(
        ForeignKey("instances.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    base_currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    username: Mapped[str]
    password: Mapped[str]
    leverage: Mapped[int]
    balance: Mapped[Decimal] = mapped_column(Numeric(18, 6), default=Decimal(0))
    account_type: Mapped[str]
    status: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(default=None)

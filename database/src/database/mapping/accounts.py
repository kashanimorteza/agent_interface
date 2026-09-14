from decimal import Decimal

from model import Account, AccountGroup
from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..foundation import StorageBase
from . import register


@register(AccountGroup)
class AccountGroupRow(StorageBase):
    __tablename__ = "account_groups"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_account_groups_user_id_name"),
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


@register(Account)
class AccountRow(StorageBase):
    __tablename__ = "accounts"
    __table_args__ = (
        UniqueConstraint("name", name="uq_accounts_name"),
        UniqueConstraint(
            "group_id",
            "broker_id",
            "instance_id",
            name="uq_accounts_group_id_broker_id_instance_id",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("account_groups.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    broker_id: Mapped[int] = mapped_column(
        ForeignKey("brokers.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    instance_id: Mapped[int] = mapped_column(
        ForeignKey("instances.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    base_currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    leverage: Mapped[int] = mapped_column(nullable=False)
    balance: Mapped[Decimal] = mapped_column(
        Numeric, nullable=False, default=Decimal(0)
    )
    account_type: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

from model import Asset, Broker, Currency
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..foundation import StorageBase
from . import register


@register(Currency)
class CurrencyRow(StorageBase):
    __tablename__ = "currencies"
    __table_args__ = (
        UniqueConstraint("user_id", "code", name="uq_currencies_user_id_code"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(nullable=False)
    symbol: Mapped[str | None] = mapped_column(nullable=True)
    country: Mapped[str | None] = mapped_column(nullable=True)
    decimal_digits: Mapped[int] = mapped_column(nullable=False, default=2)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(nullable=True)


@register(Broker)
class BrokerRow(StorageBase):
    __tablename__ = "brokers"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_brokers_user_id_name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(nullable=True)


@register(Asset)
class AssetRow(StorageBase):
    __tablename__ = "assets"
    __table_args__ = (
        UniqueConstraint("broker_id", "symbol", name="uq_assets_broker_id_symbol"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    broker_id: Mapped[int] = mapped_column(
        ForeignKey("brokers.id", ondelete="RESTRICT", onupdate="RESTRICT"),
        nullable=False,
        index=True,
    )
    symbol: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    point_size: Mapped[float] = mapped_column(nullable=False, default=0.0)
    digits: Mapped[int] = mapped_column(nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

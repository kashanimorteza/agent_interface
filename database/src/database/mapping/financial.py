"""Storage mappings for Currency, Broker, and Asset."""

from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CurrencyTable(Base):
    __tablename__ = "currencies"
    __table_args__ = (UniqueConstraint("user_id", "code", name="uq_currencies_user_id_code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    code: Mapped[str] = mapped_column(String(3), nullable=False)
    symbol: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    decimal_digits: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class BrokerTable(Base):
    __tablename__ = "brokers"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_brokers_user_id_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)


class AssetTable(Base):
    __tablename__ = "assets"
    __table_args__ = (UniqueConstraint("broker_id", "symbol", name="uq_assets_broker_id_symbol"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    broker_id: Mapped[int] = mapped_column(
        ForeignKey("brokers.id", onupdate="RESTRICT", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    point_size: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    digits: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

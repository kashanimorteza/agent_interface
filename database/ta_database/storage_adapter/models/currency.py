from __future__ import annotations

from sqlalchemy import Boolean, Integer, String, UniqueConstraint, true
from sqlalchemy.orm import Mapped, mapped_column

from ta_database.storage_adapter.base import Base


class Currency(Base):
    __tablename__ = "currencies"
    __table_args__ = (UniqueConstraint("code", name="uq_currencies_code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String(3), nullable=False)
    symbol: Mapped[str | None] = mapped_column(String, nullable=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    decimal_digits: Mapped[int] = mapped_column(Integer, nullable=False, default=2, server_default="2")
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=true())
    description: Mapped[str | None] = mapped_column(String, nullable=True)

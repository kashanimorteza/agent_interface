from __future__ import annotations

from sqlalchemy import Boolean, Float, Integer, String, UniqueConstraint, true
from sqlalchemy.orm import Mapped, mapped_column

from ta_database.storage_adapter.base import Base


class Asset(Base):
    __tablename__ = "assets"
    __table_args__ = (
        UniqueConstraint("name", name="uq_assets_name"),
        UniqueConstraint("symbol", name="uq_assets_symbol"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    point_size: Mapped[float] = mapped_column(Float, nullable=False, default=0.0, server_default="0.0")
    digits: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=true())
    description: Mapped[str | None] = mapped_column(String, nullable=True)

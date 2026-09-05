from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, UniqueConstraint, true
from sqlalchemy.orm import Mapped, mapped_column

from ta_database.storage_adapter.base import Base


class Broker(Base):
    __tablename__ = "brokers"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_brokers_user_id_name"),
        Index("ix_brokers_user_id", "user_id"),
        Index("ix_brokers_trading_platform_id", "trading_platform_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    trading_platform_id: Mapped[int] = mapped_column(Integer, ForeignKey("trading_platforms.id", ondelete="RESTRICT", onupdate="RESTRICT"), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=true())
    description: Mapped[str | None] = mapped_column(String, nullable=True)

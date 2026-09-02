from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.trading_platform import TradingPlatform  # noqa: F401 — FK target


class Broker(Base):
    __tablename__ = "brokers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    trading_platform_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("trading_platforms.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

from sqlalchemy.orm import Mapped, mapped_column

from my_database._orm._base import Base


class TradingPlatformRow(Base):
    __tablename__ = "trading_platforms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    code: Mapped[str]
    status: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(default=None)

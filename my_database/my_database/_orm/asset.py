from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from my_database._orm._base import Base


class AssetRow(Base):
    __tablename__ = "assets"
    __table_args__ = (UniqueConstraint("broker_id", "symbol", name="uq_assets_broker_id_symbol"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    broker_id: Mapped[int] = mapped_column(
        ForeignKey("brokers.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    symbol: Mapped[str]
    category: Mapped[str]
    point_size: Mapped[float] = mapped_column(default=0.0)
    digits: Mapped[int] = mapped_column(default=0)
    status: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(default=None)

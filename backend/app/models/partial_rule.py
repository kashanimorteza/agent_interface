from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.partial_group import PartialGroup  # noqa: F401 — FK target


class PartialRule(Base):
    __tablename__ = "partial_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    partial_group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("partial_groups.id"), nullable=False
    )
    profit_threshold: Mapped[float | None] = mapped_column(Float, nullable=True)
    close_portion: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

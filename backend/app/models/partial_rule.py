from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PartialRule(Base):
    __tablename__ = "partial_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    partial_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("partial_groups.id"), nullable=False, index=True)
    profit_threshold: Mapped[float] = mapped_column(Float, nullable=False)
    close_portion: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

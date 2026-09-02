from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.trailing_group import TrailingGroup  # noqa: F401 — FK target


class TrailingRule(Base):
    __tablename__ = "trailing_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    trailing_group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("trailing_groups.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

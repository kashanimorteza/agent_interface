from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.action import Action  # noqa: F401 — FK target


class Execute(Base):
    __tablename__ = "executes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    action_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("actions.id"), nullable=False
    )
    profit: Mapped[float | None] = mapped_column(Float, nullable=True)
    state: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

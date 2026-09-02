from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Execute(Base):
    __tablename__ = "executes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    action_id: Mapped[int] = mapped_column(Integer, ForeignKey("actions.id"), nullable=False, index=True)
    profit: Mapped[float] = mapped_column(Float, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.account import Account  # noqa: F401 — FK target
from app.models.action_group import ActionGroup  # noqa: F401 — FK target
from app.models.asset import Asset  # noqa: F401 — FK target
from app.models.strategy import Strategy  # noqa: F401 — FK target


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    asset_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("assets.id"), nullable=False
    )
    account_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("accounts.id"), nullable=False
    )
    strategy_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("strategies.id"), nullable=False
    )
    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("action_groups.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

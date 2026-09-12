from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from my_database._orm._base import Base


class CurrencyRow(Base):
    __tablename__ = "currencies"
    __table_args__ = (UniqueConstraint("user_id", "code", name="uq_currencies_user_id_code"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    code: Mapped[str] = mapped_column(index=True)
    symbol: Mapped[str | None] = mapped_column(default=None)
    country: Mapped[str | None] = mapped_column(default=None)
    decimal_digits: Mapped[int] = mapped_column(default=2)
    status: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(default=None)

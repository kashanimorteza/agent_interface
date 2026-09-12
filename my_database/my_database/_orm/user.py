from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from my_database._orm._base import Base


class UserRow(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("name", name="uq_users_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    api_key: Mapped[str]
    status: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(default=None)

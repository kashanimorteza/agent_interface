from __future__ import annotations

from sqlalchemy import Boolean, Integer, String, UniqueConstraint, true
from sqlalchemy.orm import Mapped, mapped_column

from ta_database.storage_adapter.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("name", name="uq_users_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False, info={"credential_storage": "hash"})
    api_key: Mapped[str] = mapped_column(String, nullable=False, info={"credential_storage": "hash"})
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default=true())
    description: Mapped[str | None] = mapped_column(String, nullable=True)

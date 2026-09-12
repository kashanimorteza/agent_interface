from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from my_database._orm._base import Base


class InstanceRow(Base):
    __tablename__ = "instances"
    __table_args__ = (UniqueConstraint("user_id", "name", name="uq_instances_user_id_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    name: Mapped[str]
    trading_platform_id: Mapped[int] = mapped_column(
        ForeignKey("trading_platforms.id", onupdate="RESTRICT", ondelete="RESTRICT"), index=True
    )
    ip: Mapped[str | None] = mapped_column(default=None)
    username: Mapped[str | None] = mapped_column(default=None)
    password: Mapped[str | None] = mapped_column(default=None)
    api_key: Mapped[str | None] = mapped_column(default=None)
    status: Mapped[bool] = mapped_column(default=True)
    description: Mapped[str | None] = mapped_column(default=None)

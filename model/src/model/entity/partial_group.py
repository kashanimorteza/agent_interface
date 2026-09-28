"""Partial Group Entity."""

from model.declaration import Declaration
from model.entity.user import User
from model.foundation import Foundation


class PartialGroup(Foundation, table=True):
    """Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds."""

    id: int | None = Declaration.identity()
    user_id: int = Declaration.field(
        reference=User, description="Identifies the user who owns the partial group."
    )
    name: str = Declaration.field(description="The partial group's display name.")
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the partial group is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the partial group."
    )

    __table_args__ = Declaration.composite(
        "PartialGroup", unique=(("user_id", "name"),)
    )

"""Trailing Group Entity."""

from model.declaration import Declaration
from model.entity.user import User
from model.foundation import Foundation


class TrailingGroup(Foundation, table=True):
    """Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply."""

    id: int | None = Declaration.identity()
    user_id: int = Declaration.field(
        reference=User, description="Identifies the user who owns the trailing group."
    )
    name: str = Declaration.field(description="The trailing group's display name.")
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the trailing group is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the trailing group."
    )

    __table_args__ = Declaration.composite(
        "TrailingGroup", unique=(("user_id", "name"),)
    )

"""Action Group Entity."""

from model.declaration import Declaration
from model.entity.user import User
from model.foundation import Foundation


class ActionGroup(Foundation, table=True):
    """Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level."""

    id: int | None = Declaration.identity()
    user_id: int = Declaration.field(
        reference=User, description="Identifies the user who owns the action group."
    )
    name: str = Declaration.field(description="The action group's display name.")
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the action group is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the action group."
    )

    __table_args__ = Declaration.composite("ActionGroup", unique=(("user_id", "name"),))

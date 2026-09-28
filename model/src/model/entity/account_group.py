"""Account Group Entity."""

from model.declaration import Declaration
from model.entity.user import User
from model.foundation import Foundation


class AccountGroup(Foundation, table=True):
    """Defines an independent group for organizing trading accounts owned by one user."""

    id: int | None = Declaration.identity()
    user_id: int = Declaration.field(
        reference=User, description="Identifies the user who owns the account group."
    )
    name: str = Declaration.field(description="The account group's display name.")
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the account group is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the account group."
    )

    __table_args__ = Declaration.composite(
        "AccountGroup", unique=(("user_id", "name"),)
    )

"""Broker Entity."""

from model.declaration import Declaration
from model.entity.user import User
from model.foundation import Foundation


class Broker(Foundation, table=True):
    """Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform."""

    id: int | None = Declaration.identity()
    name: str = Declaration.field(description="The broker's display name.")
    user_id: int = Declaration.field(
        reference=User,
        description="Identifies the user who owns the broker configuration.",
    )
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the broker is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the broker."
    )

    __table_args__ = Declaration.composite("Broker", unique=(("user_id", "name"),))

"""The Trailing Group Domain Definition: an independent group of Stop Loss / Take Profit trailing rules."""

from typing import ClassVar

from model.foundation import DomainModel, domain_field


class TrailingGroup(DomainModel):
    """A group, owned by a User, identifying the rule set that manages Stop Loss and Take Profit during a trade."""

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the trailing group.",
    )
    user_id: int = domain_field(
        foreign_key="User.id",
        cardinality="many_to_one",
        description="Identifies the user who owns the trailing group.",
    )
    name: str = domain_field(description="The trailing group's display name.")
    is_active: bool = domain_field(
        default=True, description="Indicates whether the trailing group is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the trailing group."
    )

"""The Partial Group Domain Definition: an independent group of partial-close rules."""

from typing import ClassVar

from model.foundation import DomainModel, domain_field


class PartialGroup(DomainModel):
    """A group, owned by a User, whose rules determine how much of a trade's volume to close at given thresholds."""

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the partial group.",
    )
    user_id: int = domain_field(
        foreign_key="User.id",
        cardinality="many_to_one",
        description="Identifies the user who owns the partial group.",
    )
    name: str = domain_field(description="The partial group's display name.")
    is_active: bool = domain_field(
        default=True, description="Indicates whether the partial group is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the partial group."
    )

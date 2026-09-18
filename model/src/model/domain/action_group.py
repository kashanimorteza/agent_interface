"""The Action Group Domain Definition: an independent grouping for trading actions by risk profile."""

from typing import ClassVar

from model.foundation import DomainModel, domain_field


class ActionGroup(DomainModel):
    """A group, owned by a User, organizing trading Actions by their intended risk level."""

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the action group.",
    )
    user_id: int = domain_field(
        foreign_key="User.id",
        cardinality="many_to_one",
        description="Identifies the user who owns the action group.",
    )
    name: str = domain_field(description="The action group's display name.")
    is_active: bool = domain_field(
        default=True, description="Indicates whether the action group is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the action group."
    )

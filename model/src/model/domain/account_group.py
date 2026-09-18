"""The Account Group Domain Definition: an independent group for organizing trading accounts."""

from typing import ClassVar

from model.foundation import DomainModel, domain_field


class AccountGroup(DomainModel):
    """A group, owned by a User, for organizing trading accounts."""

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the account group.",
    )
    user_id: int = domain_field(
        foreign_key="User.id",
        cardinality="many_to_one",
        description="Identifies the user who owns the account group.",
    )
    name: str = domain_field(description="The account group's display name.")
    is_active: bool = domain_field(
        default=True, description="Indicates whether the account group is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the account group."
    )

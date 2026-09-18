"""The Broker Domain Definition: a broker supported by the system."""

from typing import ClassVar

from model.foundation import DomainModel, domain_field


class Broker(DomainModel):
    """A broker, owned by a User, kept independent of any one Trading Platform."""

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the broker.",
    )
    name: str = domain_field(description="The broker's display name.")
    user_id: int = domain_field(
        foreign_key="User.id",
        cardinality="many_to_one",
        description="Identifies the user who owns the broker configuration.",
    )
    is_active: bool = domain_field(
        default=True, description="Indicates whether the broker is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the broker."
    )

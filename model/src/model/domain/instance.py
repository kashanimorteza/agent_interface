"""The Instance Domain Definition: a user-owned connection to a supported Trading Platform."""

from typing import ClassVar

from model.foundation import DomainModel, domain_field


class Instance(DomainModel):
    """A user-owned connection instance through which the system accesses a Trading Platform."""

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: int | None = domain_field(
        default=None,
        primary_key=True,
        auto_increment=True,
        nullable=False,
        description="Identifies the instance.",
    )
    user_id: int = domain_field(
        foreign_key="User.id",
        cardinality="many_to_one",
        description="Identifies the user who owns this instance.",
    )
    trading_platform_id: int = domain_field(
        foreign_key="TradingPlatform.id",
        cardinality="many_to_one",
        description="Identifies the trading platform used by this instance.",
    )
    name: str = domain_field(description="The instance's display name.")
    ip: str | None = domain_field(
        default=None,
        description="Identifies the technical network address used to reach the Trading Platform when required.",
    )
    username: str | None = domain_field(
        default=None,
        description="Defines the technical username used to establish the Instance connection.",
    )
    password: str | None = domain_field(
        default=None,
        credential="encrypted",
        description="Defines the technical password used to establish the Instance connection.",
    )
    api_key: str | None = domain_field(
        default=None,
        credential="encrypted",
        description="Defines the technical API credential used to establish the Instance connection.",
    )
    is_active: bool = domain_field(
        default=True, description="Indicates whether the instance is active."
    )
    description: str | None = domain_field(
        default=None, description="Describes the instance."
    )

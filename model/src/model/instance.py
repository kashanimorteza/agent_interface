"""The Instance Domain Definition."""

from __future__ import annotations

from typing import ClassVar

from model.foundation import CredentialTreatment, ModelBase, persistence_field


class Instance(ModelBase):
    """A user-owned connection instance through which the system accesses a supported Trading Platform.

    The Trading Platform selected through ``trading_platform_id`` defines
    which technical connection fields this Instance actually requires before
    it can be used. Evaluating that conditional requirement needs the
    referenced Trading Platform's own data together with operation-specific
    context, so it is resolved by the Component that carries that context
    rather than by Model's Intrinsic validation; Model preserves the
    relationship and every connection field the requirement may draw on.
    """

    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: int = persistence_field(
        primary_key=True,
        auto_increment=True,
        description="Primary identity of the instance.",
    )
    user_id: int = persistence_field(
        foreign_key="user.id", description="Identifies the user who owns this instance."
    )
    trading_platform_id: int = persistence_field(
        foreign_key="trading_platform.id",
        description="Identifies the trading platform used by this instance.",
    )
    name: str = persistence_field(description="The instance's display name.")
    ip: str | None = persistence_field(
        default=None,
        description="Identifies the technical network address used to reach the Trading Platform when required.",
    )
    username: str | None = persistence_field(
        default=None,
        description="Defines the technical username used to establish the Instance connection when required.",
    )
    password: str | None = persistence_field(
        default=None,
        credential=CredentialTreatment.ENCRYPTED,
        description="Defines the technical password used to establish the Instance connection when required.",
    )
    api_key: str | None = persistence_field(
        default=None,
        credential=CredentialTreatment.ENCRYPTED,
        description="Defines the technical API credential used to establish the Instance connection when required.",
    )
    is_active: bool = persistence_field(
        default=True, description="Indicates whether the instance is active."
    )
    description: str | None = persistence_field(
        default=None, description="Describes the instance."
    )

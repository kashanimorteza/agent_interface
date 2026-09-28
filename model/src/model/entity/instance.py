"""Instance Entity."""

from model.declaration import Declaration, Sensitivity
from model.entity.trading_platform import TradingPlatform
from model.entity.user import User
from model.foundation import Foundation


class Instance(Foundation, table=True):
    """Defines a user-owned connection instance through which the system accesses a supported Trading Platform."""

    id: int | None = Declaration.identity()
    user_id: int = Declaration.field(
        reference=User, description="Identifies the user who owns this instance."
    )
    trading_platform_id: int = Declaration.field(
        reference=TradingPlatform,
        description="Identifies the trading platform used by this instance.",
    )
    name: str = Declaration.field(description="The instance's display name.")
    ip: str | None = Declaration.field(
        nullable=True,
        description="Identifies the technical network address used to reach the Trading Platform when required.",
    )
    username: str | None = Declaration.field(
        nullable=True,
        description="Defines the technical username used to establish the Instance connection when required.",
    )
    password: str | None = Declaration.field(
        nullable=True,
        sensitivity=Sensitivity.PASSWORD,
        description="Defines the technical password used to establish the Instance connection when required.",
    )
    api_key: str | None = Declaration.field(
        nullable=True,
        sensitivity=Sensitivity.SENSITIVE,
        description="Defines the technical API credential used to establish the Instance connection when required.",
    )
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the instance is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the instance."
    )

    __table_args__ = Declaration.composite("Instance", unique=(("user_id", "name"),))

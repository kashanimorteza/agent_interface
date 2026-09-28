"""Currency Entity."""

from model.declaration import Declaration
from model.entity.user import User
from model.foundation import Foundation


class Currency(Foundation, table=True):
    """Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision."""

    id: int | None = Declaration.identity()
    user_id: int = Declaration.field(
        reference=User, description="Identifies the user who owns this currency."
    )
    code: str = Declaration.field(
        length=3,
        description="The currency's standard three-letter code, such as `USD` or `EUR`.",
    )
    symbol: str | None = Declaration.field(
        nullable=True,
        description="The currency's display symbol, such as `$`, `€`, or `£`.",
    )
    country: str | None = Declaration.field(
        nullable=True,
        description="Identifies the country or region associated with the currency.",
    )
    decimal_digits: int = Declaration.field(
        default=2,
        description="Defines the number of decimal digits normally used for monetary values in the currency.",
    )
    is_active: bool = Declaration.field(
        default=True, description="Indicates whether the currency is active."
    )
    description: str | None = Declaration.field(
        nullable=True, description="Describes the currency."
    )

    __table_args__ = Declaration.composite("Currency", unique=(("user_id", "code"),))

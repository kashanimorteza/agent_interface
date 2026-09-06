"""The Asset Model."""

from collections.abc import Mapping
from typing import Annotated, ClassVar

from ._base import Model
from ._spec import FieldSpec, LogicalType


class Asset(Model):
    """Defines an asset that can be selected for trading. It provides the system with the complete set
    of available tradable assets and identifies the category of each asset so the system knows
    exactly what is being traded.
    """

    logical_key: ClassVar[str] = "asset"
    logical_purpose: ClassVar[str] = (
        "Defines an asset that can be selected for trading. It provides the system with the complete set of "
        "available tradable assets and identifies the category of each asset so the system knows exactly what "
        "is being traded."
    )
    logical_initial_data: ClassVar[tuple[Mapping[str, object], ...]] = (
        {"name": "EURUSD", "symbol": "EUR/USD", "category": "Currency", "point_size": 0.0001, "digits": 5},
        {"name": "EURGBP", "symbol": "EUR/GBP", "category": "Currency", "point_size": 0.001, "digits": 5},
        {"name": "XAUUSD", "symbol": "XAU/USD", "category": "Commodity", "point_size": 0.01, "digits": 2},
        {"name": "USOil", "symbol": "USOil", "category": "Commodity", "point_size": 0.01, "digits": 3},
    )

    id: Annotated[
        int | None,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            auto_increment=True,
            primary_key=True,
        ),
    ] = None
    name: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            unique=True,
            purpose="The asset's display name.",
        ),
    ]
    symbol: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            unique=True,
            purpose="Identifies the tradable asset, such as EUR/USD, XAU/USD, or USOil.",
        ),
    ]
    category: Annotated[
        str,
        FieldSpec(
            type=LogicalType.string,
            nullable=False,
            purpose="Identifies the asset category, such as Currency, Commodity, or Cryptocurrency.",
        ),
    ]
    point_size: Annotated[
        float,
        FieldSpec(
            type=LogicalType.float,
            nullable=False,
            default=0.0,
            purpose="Stores the size of one point for the asset.",
        ),
    ] = 0.0
    digits: Annotated[
        int,
        FieldSpec(
            type=LogicalType.integer,
            nullable=False,
            default=0,
            purpose="Stores the number of decimal digits used for the asset's price.",
        ),
    ] = 0
    status: Annotated[
        bool,
        FieldSpec(
            type=LogicalType.boolean,
            nullable=False,
            default=True,
            purpose="Indicates whether the asset is active.",
        ),
    ] = True
    description: Annotated[
        str | None,
        FieldSpec(
            type=LogicalType.string,
            nullable=True,
            purpose="Describes the asset.",
        ),
    ] = None

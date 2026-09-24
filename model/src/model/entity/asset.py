"""The Asset Domain Definition."""

from typing import Annotated

from model.entity.broker import Broker
from model.foundation import (
    Constraint,
    Declare,
    FiniteFloat,
    ModelFoundation,
    Relationship,
)

__all__ = ["Asset"]


class Asset(
    ModelFoundation,
    description="Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.",
    persistent="persistent",
    relationships=(
        Relationship(
            name="broker",
            description="Belongs to one Broker through `broker_id`.",
            definition=Broker,
            cardinality="1",
            optional=False,
        ),
    ),
    composite_constraints=(
        Constraint(
            id="asset_broker_id_symbol_unique",
            description="The combination of `broker_id` and `symbol` must be unique.",
        ),
    ),
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the asset.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    broker_id: Annotated[
        int,
        Declare(
            description="Identifies the broker that provides this asset.",
            logical_type="integer",
        ),
    ]
    symbol: Annotated[
        str,
        Declare(
            description="Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`.",
            logical_type="string",
        ),
    ]
    category: Annotated[
        str,
        Declare(
            description="Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`.",
            logical_type="string",
        ),
    ]
    point_size: Annotated[
        FiniteFloat,
        Declare(
            description="Stores the size of one point for the asset.",
            logical_type="float",
        ),
    ] = 0.0
    digits: Annotated[
        int,
        Declare(
            description="Stores the number of decimal digits used for the asset's price.",
            logical_type="integer",
        ),
    ] = 0
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the asset is active.", logical_type="boolean"
        ),
    ] = True
    description: Annotated[
        str | None, Declare(description="Describes the asset.", logical_type="string")
    ]

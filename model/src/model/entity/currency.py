"""The Currency Domain Definition."""

from typing import Annotated

from pydantic import Field

from model.entity.user import User
from model.foundation import (
    Constraint,
    Declare,
    ModelFoundation,
    Relationship,
)

__all__ = ["Currency"]


class Currency(
    ModelFoundation,
    description="Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.",
    persistent="persistent",
    relationships=(
        Relationship(
            name="user",
            description="Belongs to one User through `user_id`.",
            definition=User,
            cardinality="1",
            optional=False,
        ),
    ),
    composite_constraints=(
        Constraint(
            id="currency_user_id_code_unique",
            description="The combination of `user_id` and `code` must be unique.",
        ),
    ),
):
    id: Annotated[
        int,
        Declare(
            description="The unique identity of the currency.",
            logical_type="integer",
            identity=True,
            generated=True,
        ),
    ]
    user_id: Annotated[
        int,
        Declare(
            description="Identifies the user who owns this currency.",
            logical_type="integer",
        ),
    ]
    code: Annotated[
        str,
        Field(max_length=3),
        Declare(
            description="The currency's standard three-letter code, such as `USD` or `EUR`.",
            logical_type="string",
            length=3,
        ),
    ]
    symbol: Annotated[
        str | None,
        Declare(
            description="The currency's display symbol, such as `$`, `€`, or `£`.",
            logical_type="string",
        ),
    ]
    country: Annotated[
        str | None,
        Declare(
            description="Identifies the country or region associated with the currency.",
            logical_type="string",
        ),
    ]
    decimal_digits: Annotated[
        int,
        Declare(
            description="Defines the number of decimal digits normally used for monetary values in the currency.",
            logical_type="integer",
        ),
    ] = 2
    is_active: Annotated[
        bool,
        Declare(
            description="Indicates whether the currency is active.",
            logical_type="boolean",
        ),
    ] = True
    description: Annotated[
        str | None,
        Declare(description="Describes the currency.", logical_type="string"),
    ]

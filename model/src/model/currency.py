"""The Currency Domain Definition.

A currency the trading system can use, with its code, symbol, region, and monetary precision.

Choices where the Target is silent: declared persistent, because the Target gives the concept a
generated identity and stored records; `id` has no value until it is produced; text Fields carry
no length bound unless the Target states one; a nullable Field has no default and must be
supplied explicitly.
"""

from typing import Annotated

from pydantic import Field

from model.declaration import (
    Activation,
    Cardinality,
    Generated,
    Identity,
    Persistence,
    Relationship,
)
from model.foundation import ModelFoundation
from model.user import User


class Currency(ModelFoundation):
    persistence = Persistence.PERSISTENT
    relationships = (
        Relationship(
            name="user",
            via="user_id",
            reference=User,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    )
    unique_sets = (("user_id", "code"),)

    id: Annotated[int | None, Identity(), Generated()] = None
    user_id: int
    code: Annotated[str, Field(max_length=3)]
    symbol: str | None
    country: str | None
    decimal_digits: int = 2
    is_active: Annotated[bool, Activation()] = True
    description: str | None

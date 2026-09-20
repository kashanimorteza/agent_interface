"""The Asset Domain Definition.

A tradable asset a broker provides, with its category and price precision.

Choices where the Target is silent: declared persistent, because the Target gives the concept a
generated identity and stored records; `id` has no value until it is produced; text Fields carry
no length bound unless the Target states one; a nullable Field has no default and must be
supplied explicitly.
"""

from typing import Annotated

from model.broker import Broker
from model.declaration import (
    Activation,
    Cardinality,
    Generated,
    Identity,
    Persistence,
    Relationship,
)
from model.foundation import ModelFoundation


class Asset(ModelFoundation):
    persistence = Persistence.PERSISTENT
    relationships = (
        Relationship(
            name="broker",
            via="broker_id",
            reference=Broker,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    )
    unique_sets = (("broker_id", "symbol"),)

    id: Annotated[int | None, Identity(), Generated()] = None
    broker_id: int
    symbol: str
    category: str
    point_size: float = 0.0
    digits: int = 0
    is_active: Annotated[bool, Activation()] = True
    description: str | None

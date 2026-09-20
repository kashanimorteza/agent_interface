"""The PartialRule Domain Definition.

One rule that says under which condition, and how much of, a position is closed.

Choices where the Target is silent: declared persistent, because the Target gives the concept a
generated identity and stored records; `id` has no value until it is produced; text Fields carry
no length bound unless the Target states one; a nullable Field has no default and must be
supplied explicitly. Monetary and rate values are exact decimals.
"""

from typing import Annotated

from model.declaration import (
    Activation,
    Cardinality,
    Generated,
    Identity,
    Persistence,
    Relationship,
    Unique,
)
from model.foundation import ExactDecimal, ModelFoundation
from model.partial_group import PartialGroup


class PartialRule(ModelFoundation):
    persistence = Persistence.PERSISTENT
    relationships = (
        Relationship(
            name="partial_group",
            via="partial_group_id",
            reference=PartialGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    )
    unique_sets = (("partial_group_id", "profit_percentage"),)

    id: Annotated[int | None, Identity(), Generated()] = None
    name: Annotated[str, Unique()]
    partial_group_id: int
    profit_percentage: ExactDecimal
    close_percentage: ExactDecimal
    is_active: Annotated[bool, Activation()] = True
    description: str | None

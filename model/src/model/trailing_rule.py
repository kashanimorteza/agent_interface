"""The TrailingRule Domain Definition.

One rule that says when and how to adjust Take Profit and Stop Loss.

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
from model.trailing_group import TrailingGroup


class TrailingRule(ModelFoundation):
    persistence = Persistence.PERSISTENT
    relationships = (
        Relationship(
            name="trailing_group",
            via="trailing_group_id",
            reference=TrailingGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    )
    unique_sets = (("trailing_group_id", "trigger_percentage"),)

    id: Annotated[int | None, Identity(), Generated()] = None
    name: Annotated[str, Unique()]
    trailing_group_id: int
    trigger_percentage: ExactDecimal
    take_profit_adjustment: ExactDecimal | None
    stop_loss_adjustment: ExactDecimal | None
    is_active: Annotated[bool, Activation()] = True
    description: str | None

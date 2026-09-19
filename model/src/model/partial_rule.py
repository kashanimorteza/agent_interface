"""PartialRule Domain Definition.

The authoritative definition of the concept below. Modelling choices the Target leaves unstated are recorded here,
beside the Fields they belong to.

Recorded modelling choices:
* Text values carry no length bound: the Target states none.
* Both percentages are exact decimal values with no declared precision, because the Target states type `decimal` and no precision.
"""

from typing import Annotated

from model.foundation import (
    ActiveFlag,
    ExactDecimal,
    GeneratedIdentity,
    ModelFoundation,
)
from model.partial_group import PartialGroup
from model.vocabulary import Cardinality, Persistence, Reference, Unique


class PartialRule(ModelFoundation):
    """An individual Partial Close rule: the profit condition under which part of an open position is closed and how much of its volume."""

    persistence = Persistence.PERSISTENT
    unique_sets = (("partial_group_id", "profit_percentage"),)

    id: GeneratedIdentity = None
    name: Annotated[str, Unique()]
    partial_group_id: Annotated[
        int,
        Reference(
            definition=PartialGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    ]
    profit_percentage: ExactDecimal
    close_percentage: ExactDecimal
    is_active: ActiveFlag = True
    description: str | None = None

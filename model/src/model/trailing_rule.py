"""TrailingRule Domain Definition.

The authoritative definition of the concept below. Modelling choices the Target leaves unstated are recorded here,
beside the Fields they belong to.

Recorded modelling choices:
* Text values carry no length bound: the Target states none.
* All percentages and adjustments are exact decimal values with no declared precision, because the Target states type `decimal` and no precision.
"""

from decimal import Decimal
from typing import Annotated

from pydantic import Field

from model.foundation import (
    ActiveFlag,
    ExactDecimal,
    GeneratedIdentity,
    ModelFoundation,
)
from model.trailing_group import TrailingGroup
from model.vocabulary import Cardinality, Persistence, Reference, Unique

OptionalExactDecimal = Annotated[Decimal | None, Field(strict=False)]
"""An exact decimal value that may be absent; its Plain Representation is text."""


class TrailingRule(ModelFoundation):
    """An individual rule within a Trailing Group that says when and how Take Profit and Stop Loss are adjusted."""

    persistence = Persistence.PERSISTENT
    unique_sets = (("trailing_group_id", "trigger_percentage"),)

    id: GeneratedIdentity = None
    name: Annotated[str, Unique()]
    trailing_group_id: Annotated[
        int,
        Reference(
            definition=TrailingGroup,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    ]
    trigger_percentage: ExactDecimal
    take_profit_adjustment: OptionalExactDecimal = None
    stop_loss_adjustment: OptionalExactDecimal = None
    is_active: ActiveFlag = True
    description: str | None = None

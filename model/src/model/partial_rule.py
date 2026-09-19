from decimal import Decimal
from typing import Annotated, ClassVar

from model.foundation import Declare, DomainDefinition, GeneratedId, Reference


class PartialRule(DomainDefinition):
    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (
        ("partial_group_id", "profit_percentage"),
    )

    id: GeneratedId = None
    name: Annotated[str, Declare("string", unique=True)]
    partial_group_id: Annotated[
        int, Declare("integer", references=Reference("PartialGroup"))
    ]
    profit_percentage: Annotated[Decimal, Declare("decimal")]
    close_percentage: Annotated[Decimal, Declare("decimal")]
    is_active: Annotated[bool, Declare("boolean")] = True
    description: Annotated[str | None, Declare("string")] = None

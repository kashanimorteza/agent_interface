from typing import Annotated, ClassVar

from pydantic import StringConstraints

from model.foundation import Declare, DomainDefinition, GeneratedId, Reference


class Currency(DomainDefinition):
    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "code"),)

    id: GeneratedId = None
    user_id: Annotated[int, Declare("integer", references=Reference("User"))]
    code: Annotated[str, StringConstraints(max_length=3), Declare("string", length=3)]
    symbol: Annotated[str | None, Declare("string")] = None
    country: Annotated[str | None, Declare("string")] = None
    decimal_digits: Annotated[int, Declare("integer")] = 2
    is_active: Annotated[bool, Declare("boolean")] = True
    description: Annotated[str | None, Declare("string")] = None

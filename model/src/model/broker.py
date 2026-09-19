from typing import Annotated, ClassVar

from model.foundation import Declare, DomainDefinition, GeneratedId, Reference


class Broker(DomainDefinition):
    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: GeneratedId = None
    name: Annotated[str, Declare("string")]
    user_id: Annotated[int, Declare("integer", references=Reference("User"))]
    is_active: Annotated[bool, Declare("boolean")] = True
    description: Annotated[str | None, Declare("string")] = None

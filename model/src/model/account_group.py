from typing import Annotated, ClassVar

from model.foundation import Declare, DomainDefinition, GeneratedId, Reference


class AccountGroup(DomainDefinition):
    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: GeneratedId = None
    user_id: Annotated[int, Declare("integer", references=Reference("User"))]
    name: Annotated[str, Declare("string")]
    is_active: Annotated[bool, Declare("boolean")] = True
    description: Annotated[str | None, Declare("string")] = None

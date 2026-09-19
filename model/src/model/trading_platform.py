from typing import Annotated, ClassVar

from model.foundation import Declare, DomainDefinition, GeneratedId


class TradingPlatform(DomainDefinition):
    persistent: ClassVar[bool] = True

    id: GeneratedId = None
    name: Annotated[str, Declare("string", unique=True)]
    code: Annotated[str, Declare("string")]
    is_active: Annotated[bool, Declare("boolean")] = True
    description: Annotated[str | None, Declare("string")] = None

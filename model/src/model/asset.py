from typing import Annotated, ClassVar

from model.foundation import Declare, DomainDefinition, GeneratedId, Reference


class Asset(DomainDefinition):
    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("broker_id", "symbol"),)

    id: GeneratedId = None
    broker_id: Annotated[int, Declare("integer", references=Reference("Broker"))]
    symbol: Annotated[str, Declare("string")]
    category: Annotated[str, Declare("string")]
    point_size: Annotated[float, Declare("float")] = 0.0
    digits: Annotated[int, Declare("integer")] = 0
    is_active: Annotated[bool, Declare("boolean")] = True
    description: Annotated[str | None, Declare("string")] = None

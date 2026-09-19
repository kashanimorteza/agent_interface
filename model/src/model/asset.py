"""Asset Domain Definition.

The authoritative definition of the concept below. Modelling choices the Target leaves unstated are recorded here,
beside the Fields they belong to.

Recorded modelling choices:
* Text values carry no length bound: the Target states none.
* `point_size` is a floating-point number because the Target states type `float` for it.
"""

from typing import Annotated

from model.broker import Broker
from model.foundation import ActiveFlag, GeneratedIdentity, ModelFoundation
from model.vocabulary import Cardinality, Persistence, Reference


class Asset(ModelFoundation):
    """An asset that can be selected for trading, with the category that tells the system what is being traded."""

    persistence = Persistence.PERSISTENT
    unique_sets = (("broker_id", "symbol"),)

    id: GeneratedIdentity = None
    broker_id: Annotated[
        int,
        Reference(
            definition=Broker, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    symbol: str
    category: str
    point_size: float = 0.0
    digits: int = 0
    is_active: ActiveFlag = True
    description: str | None = None

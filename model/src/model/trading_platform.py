"""TradingPlatform Domain Definition.

The authoritative definition of the concept below. Modelling choices the Target leaves unstated are recorded here,
beside the Fields they belong to.

Recorded modelling choices:
* Text values carry no length bound: the Target states none.
"""

from typing import Annotated

from model.foundation import ActiveFlag, GeneratedIdentity, ModelFoundation
from model.vocabulary import Persistence, Unique


class TradingPlatform(ModelFoundation):
    """A supported trading API standard, kept independent of any specific exchange or broker."""

    persistence = Persistence.PERSISTENT

    id: GeneratedIdentity = None
    name: Annotated[str, Unique()]
    code: str
    is_active: ActiveFlag = True
    description: str | None = None

"""Currency Domain Definition.

The authoritative definition of the concept below. Modelling choices the Target leaves unstated are recorded here,
beside the Fields they belong to.

Recorded modelling choices:
* Text values carry no length bound: the Target states none.
* `code` is held at exactly three characters: the Target states size 3 for a three-letter standard code.
"""

from typing import Annotated

from pydantic import Field

from model.foundation import ActiveFlag, GeneratedIdentity, ModelFoundation
from model.user import User
from model.vocabulary import Cardinality, Persistence, Reference


class Currency(ModelFoundation):
    """A currency the trading system can use, with its standard code, display symbol, country or region, and monetary decimal precision."""

    persistence = Persistence.PERSISTENT
    unique_sets = (("user_id", "code"),)

    id: GeneratedIdentity = None
    user_id: Annotated[
        int,
        Reference(
            definition=User, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    code: Annotated[str, Field(min_length=3, max_length=3)]
    symbol: str | None = None
    country: str | None = None
    decimal_digits: int = 2
    is_active: ActiveFlag = True
    description: str | None = None

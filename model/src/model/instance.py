"""Instance Domain Definition.

The authoritative definition of the concept below. Modelling choices the Target leaves unstated are recorded here,
beside the Fields they belong to.

Recorded modelling choices:
* Text values carry no length bound: the Target states none.
"""

from typing import Annotated

from model.foundation import ActiveFlag, GeneratedIdentity, ModelFoundation
from model.trading_platform import TradingPlatform
from model.user import User
from model.vocabulary import (
    AtRestTreatment,
    Cardinality,
    Credential,
    Persistence,
    Reference,
)


class Instance(ModelFoundation):
    """A user-owned connection instance through which the system accesses a supported Trading Platform.

    The Target rule that the Trading Platform selected for an Instance defines which connection Fields are
    required depends on data outside the Instance, so this definition does not evaluate it."""

    persistence = Persistence.PERSISTENT
    unique_sets = (("user_id", "name"),)

    id: GeneratedIdentity = None
    user_id: Annotated[
        int,
        Reference(
            definition=User, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    trading_platform_id: Annotated[
        int,
        Reference(
            definition=TradingPlatform,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    ]
    name: str
    ip: str | None = None
    username: str | None = None
    password: Annotated[str | None, Credential(treatment=AtRestTreatment.ENCRYPTED)] = (
        None
    )
    api_key: Annotated[str | None, Credential(treatment=AtRestTreatment.ENCRYPTED)] = (
        None
    )
    is_active: ActiveFlag = True
    description: str | None = None

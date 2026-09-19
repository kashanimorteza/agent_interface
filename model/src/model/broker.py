"""Broker Domain Definition.

The authoritative definition of the concept below. Modelling choices the Target leaves unstated are recorded here,
beside the Fields they belong to.

Recorded modelling choices:
* Text values carry no length bound: the Target states none.
"""

from typing import Annotated

from model.foundation import ActiveFlag, GeneratedIdentity, ModelFoundation
from model.user import User
from model.vocabulary import Cardinality, Persistence, Reference


class Broker(ModelFoundation):
    """A broker supported by the system, owned by one user and not coupled to any Trading Platform."""

    persistence = Persistence.PERSISTENT
    unique_sets = (("user_id", "name"),)

    id: GeneratedIdentity = None
    name: str
    user_id: Annotated[
        int,
        Reference(
            definition=User, field="id", cardinality=Cardinality.ONE, optional=False
        ),
    ]
    is_active: ActiveFlag = True
    description: str | None = None

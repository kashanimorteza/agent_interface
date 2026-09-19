"""User Domain Definition.

The authoritative definition of the concept below. Modelling choices the Target leaves unstated are recorded here,
beside the Fields they belong to.

Recorded modelling choices:
* Text values carry no length bound: the Target states none.
"""

from typing import Annotated

from model.foundation import ActiveFlag, GeneratedIdentity, ModelFoundation
from model.vocabulary import AtRestTreatment, Credential, Persistence, Unique


class User(ModelFoundation):
    """An independent user of the system. Each user has a separate set of settings, so new users can be added without affecting existing ones."""

    persistence = Persistence.PERSISTENT

    id: GeneratedIdentity = None
    name: Annotated[str, Unique()]
    username: Annotated[str, Unique()]
    password: Annotated[str, Credential(treatment=AtRestTreatment.HASH)]
    api_key: Annotated[str, Credential(treatment=AtRestTreatment.HASH)]
    is_active: ActiveFlag = True
    description: str | None = None

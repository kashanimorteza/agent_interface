"""The User Domain Definition.

An independent user of the system, so each user can have distinct settings.

Choices where the Target is silent: declared persistent, because the Target gives the concept a
generated identity and stored records; `id` has no value until it is produced; text Fields carry
no length bound unless the Target states one; a nullable Field has no default and must be
supplied explicitly.
"""

from typing import Annotated

from model.declaration import (
    Activation,
    AtRest,
    Credential,
    Generated,
    Identity,
    Persistence,
    Unique,
)
from model.foundation import ModelFoundation


class User(ModelFoundation):
    persistence = Persistence.PERSISTENT

    id: Annotated[int | None, Identity(), Generated()] = None
    name: Annotated[str, Unique()]
    username: Annotated[str, Unique()]
    password: Annotated[str, Credential(AtRest.HASH)]
    api_key: Annotated[str, Credential(AtRest.HASH)]
    is_active: Annotated[bool, Activation()] = True
    description: str | None

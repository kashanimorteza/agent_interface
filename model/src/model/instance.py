"""The Instance Domain Definition.

A user-owned connection through which the system reaches a Trading Platform.

Choices where the Target is silent: declared persistent, because the Target gives the concept a
generated identity and stored records; `id` has no value until it is produced; text Fields carry
no length bound unless the Target states one; a nullable Field has no default and must be
supplied explicitly.
"""

from typing import Annotated

from model.declaration import (
    Activation,
    AtRest,
    Cardinality,
    Credential,
    Generated,
    Identity,
    Persistence,
    Relationship,
)
from model.foundation import ModelFoundation
from model.trading_platform import TradingPlatform
from model.user import User


class Instance(ModelFoundation):
    persistence = Persistence.PERSISTENT
    relationships = (
        Relationship(
            name="user",
            via="user_id",
            reference=User,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
        Relationship(
            name="trading_platform",
            via="trading_platform_id",
            reference=TradingPlatform,
            field="id",
            cardinality=Cardinality.ONE,
            optional=False,
        ),
    )
    unique_sets = (("user_id", "name"),)

    id: Annotated[int | None, Identity(), Generated()] = None
    user_id: int
    trading_platform_id: int
    name: str
    ip: str | None
    username: str | None
    password: Annotated[str | None, Credential(AtRest.ENCRYPTED)]
    api_key: Annotated[str | None, Credential(AtRest.ENCRYPTED)]
    is_active: Annotated[bool, Activation()] = True
    description: str | None

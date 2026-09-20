"""The AccountGroup Domain Definition.

An independent group for organizing one user's trading accounts.

Choices where the Target is silent: declared persistent, because the Target gives the concept a
generated identity and stored records; `id` has no value until it is produced; text Fields carry
no length bound unless the Target states one; a nullable Field has no default and must be
supplied explicitly.
"""

from typing import Annotated

from model.declaration import (
    Activation,
    Cardinality,
    Generated,
    Identity,
    Persistence,
    Relationship,
)
from model.foundation import ModelFoundation
from model.user import User


class AccountGroup(ModelFoundation):
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
    )
    unique_sets = (("user_id", "name"),)

    id: Annotated[int | None, Identity(), Generated()] = None
    user_id: int
    name: str
    is_active: Annotated[bool, Activation()] = True
    description: str | None

"""User: an independent user of the system."""

from typing import Annotated

from .foundation import Flag, GeneratedId, HashedCredential, ModelFoundation, Text, Unique


class User(ModelFoundation):
    persistence = "persistent"

    id: GeneratedId = None
    name: Annotated[Text, Unique()]
    username: Annotated[Text, Unique()]
    password: HashedCredential
    api_key: HashedCredential
    is_active: Flag = True
    description: Text | None = None

from typing import Annotated, ClassVar

from model.foundation import CredentialText, Declare, DomainDefinition, GeneratedId


class User(DomainDefinition):
    persistent: ClassVar[bool] = True

    id: GeneratedId = None
    name: Annotated[str, Declare("string", unique=True)]
    username: Annotated[str, Declare("string", unique=True)]
    password: Annotated[CredentialText, Declare("string", credential="hash")]
    api_key: Annotated[CredentialText, Declare("string", credential="hash")]
    is_active: Annotated[bool, Declare("boolean")] = True
    description: Annotated[str | None, Declare("string")] = None

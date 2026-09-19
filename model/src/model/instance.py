from typing import Annotated, ClassVar

from model.foundation import (
    CredentialText,
    Declare,
    DomainDefinition,
    GeneratedId,
    Reference,
)


class Instance(DomainDefinition):
    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = (("user_id", "name"),)

    id: GeneratedId = None
    user_id: Annotated[int, Declare("integer", references=Reference("User"))]
    trading_platform_id: Annotated[
        int, Declare("integer", references=Reference("TradingPlatform"))
    ]
    name: Annotated[str, Declare("string")]
    ip: Annotated[str | None, Declare("string")] = None
    username: Annotated[str | None, Declare("string")] = None
    password: Annotated[
        CredentialText | None, Declare("string", credential="encrypted")
    ] = None
    api_key: Annotated[
        CredentialText | None, Declare("string", credential="encrypted")
    ] = None
    is_active: Annotated[bool, Declare("boolean")] = True
    description: Annotated[str | None, Declare("string")] = None

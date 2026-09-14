from pydantic import SecretStr

from .foundation import CredentialStorage, ModelBase, credential_field


class User(ModelBase):
    unique_together = (("name",),)

    id: int | None = None
    name: str
    username: str
    password: SecretStr = credential_field(storage=CredentialStorage.HASH)
    api_key: SecretStr = credential_field(storage=CredentialStorage.HASH)
    is_active: bool = True
    description: str | None = None


class TradingPlatform(ModelBase):
    id: int | None = None
    name: str
    code: str
    is_active: bool = True
    description: str | None = None


class Instance(ModelBase):
    unique_together = (("user_id", "name"),)

    id: int | None = None
    user_id: int
    name: str
    trading_platform_id: int
    ip: str | None = None
    username: str | None = None
    password: SecretStr | None = credential_field(
        storage=CredentialStorage.ENCRYPTED, default=None
    )
    api_key: SecretStr | None = credential_field(
        storage=CredentialStorage.ENCRYPTED, default=None
    )
    is_active: bool = True
    description: str | None = None

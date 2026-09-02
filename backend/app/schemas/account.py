from pydantic import BaseModel, ConfigDict


class AccountBase(BaseModel):
    name: str
    username: str
    password: str
    broker_id: int
    status: str
    description: str | None = None


class AccountCreate(AccountBase):
    pass


class AccountRead(AccountBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

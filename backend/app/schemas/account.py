from pydantic import BaseModel, ConfigDict


class AccountCreate(BaseModel):
    name: str
    username: str
    password: str
    broker_id: int
    status: str
    description: str | None = None


class AccountUpdate(BaseModel):
    name: str
    username: str
    password: str
    broker_id: int
    status: str
    description: str | None = None


class AccountRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    broker_id: int
    status: str
    description: str | None = None

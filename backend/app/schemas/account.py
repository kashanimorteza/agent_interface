from pydantic import BaseModel, ConfigDict


class AccountCreate(BaseModel):
    """Body of create and update — every contract field except id."""

    name: str
    username: str
    password: str
    broker_id: int
    status: str
    description: str


class AccountRead(BaseModel):
    """Response shape — every contract field with id, never password."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username: str
    broker_id: int
    status: str
    description: str

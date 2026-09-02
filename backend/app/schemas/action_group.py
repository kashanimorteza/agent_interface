from pydantic import BaseModel, ConfigDict


class ActionGroupCreate(BaseModel):
    """Body of create and update — every contract field except id."""

    name: str
    status: str
    description: str


class ActionGroupRead(BaseModel):
    """Response shape — every contract field with id."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str
    description: str

from pydantic import BaseModel, ConfigDict


class ExecuteCreate(BaseModel):
    """Body of create and update — every contract field except id."""

    name: str
    action_id: int
    profit: float
    state: str
    status: str
    description: str


class ExecuteRead(BaseModel):
    """Response shape — every contract field with id."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    action_id: int
    profit: float
    state: str
    status: str
    description: str

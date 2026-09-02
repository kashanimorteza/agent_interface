from pydantic import BaseModel, ConfigDict


class ExecuteCreate(BaseModel):
    name: str
    action_id: int
    profit: float | None = None
    state: str | None = None
    status: str
    description: str | None = None


class ExecuteUpdate(BaseModel):
    name: str
    action_id: int
    profit: float | None = None
    state: str | None = None
    status: str
    description: str | None = None


class ExecuteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    action_id: int
    profit: float | None = None
    state: str | None = None
    status: str
    description: str | None = None

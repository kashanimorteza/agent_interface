from pydantic import BaseModel, ConfigDict


class ExecuteBase(BaseModel):
    name: str
    action_id: int
    profit: float | None = None
    state: str
    status: str
    description: str | None = None


class ExecuteCreate(ExecuteBase):
    pass


class ExecuteRead(ExecuteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

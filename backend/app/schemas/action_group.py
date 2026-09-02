from pydantic import BaseModel, ConfigDict


class ActionGroupCreate(BaseModel):
    name: str
    status: str
    description: str | None = None


class ActionGroupUpdate(BaseModel):
    name: str
    status: str
    description: str | None = None


class ActionGroupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str
    description: str | None = None

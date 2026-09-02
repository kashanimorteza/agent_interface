from pydantic import BaseModel, ConfigDict


class TrailingGroupCreate(BaseModel):
    name: str
    status: str
    description: str | None = None


class TrailingGroupUpdate(BaseModel):
    name: str
    status: str
    description: str | None = None


class TrailingGroupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str
    description: str | None = None

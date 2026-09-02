from pydantic import BaseModel, ConfigDict


class PartialGroupCreate(BaseModel):
    name: str
    status: str
    description: str | None = None


class PartialGroupUpdate(BaseModel):
    name: str
    status: str
    description: str | None = None


class PartialGroupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str
    description: str | None = None

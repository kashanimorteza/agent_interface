from pydantic import BaseModel, ConfigDict


class PartialGroupBase(BaseModel):
    name: str
    status: str
    description: str | None = None


class PartialGroupCreate(PartialGroupBase):
    pass


class PartialGroupRead(PartialGroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

from pydantic import BaseModel, ConfigDict


class TrailingGroupBase(BaseModel):
    name: str
    status: str
    description: str | None = None


class TrailingGroupCreate(TrailingGroupBase):
    pass


class TrailingGroupRead(TrailingGroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

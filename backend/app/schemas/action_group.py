from pydantic import BaseModel, ConfigDict


class ActionGroupBase(BaseModel):
    name: str
    status: str
    description: str | None = None


class ActionGroupCreate(ActionGroupBase):
    pass


class ActionGroupRead(ActionGroupBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

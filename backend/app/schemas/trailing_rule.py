from pydantic import BaseModel, ConfigDict


class TrailingRuleCreate(BaseModel):
    name: str
    trailing_group_id: int
    status: str
    description: str | None = None


class TrailingRuleUpdate(BaseModel):
    name: str
    trailing_group_id: int
    status: str
    description: str | None = None


class TrailingRuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    trailing_group_id: int
    status: str
    description: str | None = None

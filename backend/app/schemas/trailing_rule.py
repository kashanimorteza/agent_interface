from pydantic import BaseModel, ConfigDict


class TrailingRuleBase(BaseModel):
    name: str
    trailing_group_id: int
    status: str
    description: str | None = None


class TrailingRuleCreate(TrailingRuleBase):
    pass


class TrailingRuleRead(TrailingRuleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

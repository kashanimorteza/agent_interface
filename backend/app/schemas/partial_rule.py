from pydantic import BaseModel, ConfigDict


class PartialRuleBase(BaseModel):
    name: str
    partial_group_id: int
    profit_threshold: float
    close_portion: float
    status: str
    description: str | None = None


class PartialRuleCreate(PartialRuleBase):
    pass


class PartialRuleRead(PartialRuleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

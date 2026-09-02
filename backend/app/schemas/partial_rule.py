from pydantic import BaseModel, ConfigDict


class PartialRuleCreate(BaseModel):
    name: str
    partial_group_id: int
    profit_threshold: float | None = None
    close_portion: float | None = None
    status: str
    description: str | None = None


class PartialRuleUpdate(BaseModel):
    name: str
    partial_group_id: int
    profit_threshold: float | None = None
    close_portion: float | None = None
    status: str
    description: str | None = None


class PartialRuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    partial_group_id: int
    profit_threshold: float | None = None
    close_portion: float | None = None
    status: str
    description: str | None = None

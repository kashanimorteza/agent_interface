from pydantic import BaseModel, ConfigDict


class PartialRuleCreate(BaseModel):
    """Body of create and update — every contract field except id."""

    name: str
    partial_group_id: int
    profit_threshold: float
    close_portion: float
    status: str
    description: str


class PartialRuleRead(BaseModel):
    """Response shape — every contract field with id."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    partial_group_id: int
    profit_threshold: float
    close_portion: float
    status: str
    description: str

from pydantic import BaseModel, ConfigDict


class TrailingRuleCreate(BaseModel):
    """Body of create and update — every contract field except id."""

    name: str
    trailing_group_id: int
    status: str
    description: str


class TrailingRuleRead(BaseModel):
    """Response shape — every contract field with id."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    trailing_group_id: int
    status: str
    description: str

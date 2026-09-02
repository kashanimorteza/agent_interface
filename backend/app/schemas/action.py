from pydantic import BaseModel, ConfigDict


class ActionCreate(BaseModel):
    """Body of create and update — every contract field except id."""

    name: str
    asset_id: int
    account_id: int
    strategy_id: int
    group_id: int
    status: str
    description: str


class ActionRead(BaseModel):
    """Response shape — every contract field with id."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    asset_id: int
    account_id: int
    strategy_id: int
    group_id: int
    status: str
    description: str

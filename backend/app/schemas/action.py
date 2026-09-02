from pydantic import BaseModel, ConfigDict


class ActionCreate(BaseModel):
    name: str
    asset_id: int
    account_id: int
    strategy_id: int
    group_id: int
    status: str
    description: str | None = None


class ActionUpdate(BaseModel):
    name: str
    asset_id: int
    account_id: int
    strategy_id: int
    group_id: int
    status: str
    description: str | None = None


class ActionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    asset_id: int
    account_id: int
    strategy_id: int
    group_id: int
    status: str
    description: str | None = None

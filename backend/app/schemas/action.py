from pydantic import BaseModel, ConfigDict


class ActionBase(BaseModel):
    name: str
    asset_id: int
    account_id: int
    strategy_id: int
    group_id: int
    status: str
    description: str | None = None


class ActionCreate(ActionBase):
    pass


class ActionRead(ActionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

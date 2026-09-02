from pydantic import BaseModel, ConfigDict


class StrategyBase(BaseModel):
    name: str
    risk_parameter: float
    status: str
    description: str | None = None


class StrategyCreate(StrategyBase):
    pass


class StrategyRead(StrategyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

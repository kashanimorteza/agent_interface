from pydantic import BaseModel, ConfigDict


class StrategyCreate(BaseModel):
    name: str
    risk_parameter: float | None = None
    status: str
    description: str | None = None


class StrategyUpdate(BaseModel):
    name: str
    risk_parameter: float | None = None
    status: str
    description: str | None = None


class StrategyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    risk_parameter: float | None = None
    status: str
    description: str | None = None

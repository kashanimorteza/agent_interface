from pydantic import BaseModel, ConfigDict


class StrategyCreate(BaseModel):
    """Body of create and update — every contract field except id."""

    name: str
    risk_parameter: float
    status: str
    description: str


class StrategyRead(BaseModel):
    """Response shape — every contract field with id."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    risk_parameter: float
    status: str
    description: str

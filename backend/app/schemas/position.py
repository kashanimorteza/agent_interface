from pydantic import BaseModel, ConfigDict


class PositionCreate(BaseModel):
    """Body of create and update — every contract field except id."""

    name: str
    entry_price: float
    take_profit: float
    stop_loss: float
    status: str
    description: str


class PositionRead(BaseModel):
    """Response shape — every contract field with id."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    entry_price: float
    take_profit: float
    stop_loss: float
    status: str
    description: str

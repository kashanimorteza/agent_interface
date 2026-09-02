from pydantic import BaseModel, ConfigDict


class PositionCreate(BaseModel):
    name: str
    entry_price: float | None = None
    take_profit: float | None = None
    stop_loss: float | None = None
    status: str
    description: str | None = None


class PositionUpdate(BaseModel):
    name: str
    entry_price: float | None = None
    take_profit: float | None = None
    stop_loss: float | None = None
    status: str
    description: str | None = None


class PositionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    entry_price: float | None = None
    take_profit: float | None = None
    stop_loss: float | None = None
    status: str
    description: str | None = None

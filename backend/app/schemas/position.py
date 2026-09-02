from pydantic import BaseModel, ConfigDict


class PositionBase(BaseModel):
    name: str
    entry_price: float
    take_profit: float
    stop_loss: float
    status: str
    description: str | None = None


class PositionCreate(PositionBase):
    pass


class PositionRead(PositionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

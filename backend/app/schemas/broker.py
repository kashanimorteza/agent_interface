from pydantic import BaseModel, ConfigDict


class BrokerCreate(BaseModel):
    """Body of create and update — every contract field except id."""

    name: str
    trading_platform_id: int
    status: str
    description: str


class BrokerRead(BaseModel):
    """Response shape — every contract field with id."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    trading_platform_id: int
    status: str
    description: str

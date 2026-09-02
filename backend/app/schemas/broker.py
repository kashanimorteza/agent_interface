from pydantic import BaseModel, ConfigDict


class BrokerBase(BaseModel):
    name: str
    trading_platform_id: int
    status: str
    description: str | None = None


class BrokerCreate(BrokerBase):
    pass


class BrokerRead(BrokerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

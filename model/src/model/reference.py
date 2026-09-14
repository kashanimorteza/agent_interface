from pydantic import Field

from .foundation import ModelBase


class Currency(ModelBase):
    unique_together = (("user_id", "code"),)

    id: int | None = None
    user_id: int
    code: str = Field(min_length=3, max_length=3)
    symbol: str | None = None
    country: str | None = None
    decimal_digits: int = 2
    is_active: bool = True
    description: str | None = None


class Broker(ModelBase):
    unique_together = (("user_id", "name"),)

    id: int | None = None
    name: str
    user_id: int
    is_active: bool = True
    description: str | None = None


class Asset(ModelBase):
    unique_together = (("broker_id", "symbol"),)

    id: int | None = None
    broker_id: int
    symbol: str
    category: str
    point_size: float = 0.0
    digits: int = 0
    is_active: bool = True
    description: str | None = None

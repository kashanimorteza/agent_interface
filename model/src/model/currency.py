"""Currency: a currency the trading system can use."""

from typing import Annotated

from pydantic import Field

from .foundation import Flag, GeneratedId, Integer, ModelFoundation, Relationship, Text
from .user import User


class Currency(ModelFoundation):
    persistence = "persistent"
    relationships = (Relationship(field="user_id", reference=User, reference_field="id", cardinality="many-to-one", optional=False),)
    unique_sets = (("user_id", "code"),)

    id: GeneratedId = None
    user_id: Integer
    code: Annotated[Text, Field(max_length=3)]
    symbol: Text | None = None
    country: Text | None = None
    decimal_digits: Integer = 2
    is_active: Flag = True
    description: Text | None = None

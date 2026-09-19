"""Trading Platform: a supported trading API standard."""

from typing import Annotated

from .foundation import Flag, GeneratedId, ModelFoundation, Text, Unique


class TradingPlatform(ModelFoundation):
    persistence = "persistent"

    id: GeneratedId = None
    name: Annotated[Text, Unique()]
    code: Text
    is_active: Flag = True
    description: Text | None = None

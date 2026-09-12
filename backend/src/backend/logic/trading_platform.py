"""The Trading Platform Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class TradingPlatformLogic(ModelLogic[m.TradingPlatform]):
    model_type = m.TradingPlatform

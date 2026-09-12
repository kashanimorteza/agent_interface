"""The Currency Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class CurrencyLogic(ModelLogic[m.Currency]):
    model_type = m.Currency

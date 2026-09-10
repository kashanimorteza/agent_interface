from __future__ import annotations

from my_model import Currency

from ._base import ModelLogic


class CurrencyLogic(ModelLogic[Currency]):
    model_cls = Currency

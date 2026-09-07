"""Logic of the Currency Model."""

from my_model import Currency

from ..base import ModelLogic


class CurrencyLogic(ModelLogic[Currency]):
    model = Currency

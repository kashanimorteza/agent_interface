from my_backend._model_interface import currency
from my_backend.logic._base import ModelLogic


class CurrencyLogic(ModelLogic[currency.Currency]):
    model_cls = currency.Currency

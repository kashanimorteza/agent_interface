"""The Currency Service."""

from model.interface import Currency

from logic.services.entity.base import EntityServiceBase


class CurrencyService(EntityServiceBase[Currency]):
    """Entity-bound Actions for Currency records."""

    entity = Currency

"""Child Service for the Currency Entity."""

from model.interface import Currency

from logic.services.entity.base_entity import BaseEntity


class CurrencyService(BaseEntity):
    """Entity-bound Actions for Currency records."""

    entity = Currency

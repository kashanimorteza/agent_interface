"""Child Service of the Currency Entity."""

from model.interface import Currency

from logic.services.entity.base_entity import BaseEntity


class CurrencyService(BaseEntity):
    """The Entity Actions bound to the Currency Entity."""

    _entity = Currency

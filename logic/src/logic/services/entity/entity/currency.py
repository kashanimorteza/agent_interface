"""Entity Child Service bound to Model's Currency Entity."""

from model.interface import Currency

from logic.services.entity.base_entity import BaseEntity


class CurrencyService(BaseEntity):
    """Selects Currency once and offers every shared Entity Action for it."""

    entity = Currency

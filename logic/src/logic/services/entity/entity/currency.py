"""Child Service of the Currency Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class Currency(BaseEntity):
    """The Entity Actions bound to the Currency Entity."""

    _entity = model.Currency

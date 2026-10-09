"""The Currency Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Currency(BaseEntity):
    """The Actions of the Currency Entity."""

    _entity = model.Currency

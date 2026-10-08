"""Currency: the Child Service bound to the Currency Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Currency(BaseEntity):
    """Works on Currency records through Storage without passing the Entity."""

    _entity = model.Currency

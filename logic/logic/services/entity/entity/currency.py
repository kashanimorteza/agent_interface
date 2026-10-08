"""The Currency Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Currency(BaseEntity):
    _entity = model.Currency

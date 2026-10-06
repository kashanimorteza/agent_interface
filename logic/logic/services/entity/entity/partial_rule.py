"""The Partial Rule Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class PartialRule(BaseEntity):
    """Child Service of the Partial Rule Entity."""

    _entity = model.PartialRule

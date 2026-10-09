"""The Partial Rule Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class PartialRule(BaseEntity):
    """The Actions of the Partial Rule Entity."""

    _entity = model.PartialRule

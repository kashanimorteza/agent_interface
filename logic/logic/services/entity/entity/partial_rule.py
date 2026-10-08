"""PartialRule: the Child Service bound to the Partial Rule Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class PartialRule(BaseEntity):
    """Works on Partial Rule records through Storage without passing the Entity."""

    _entity = model.PartialRule

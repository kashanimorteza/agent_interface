"""TrailingRule: the Child Service bound to the Trailing Rule Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TrailingRule(BaseEntity):
    """Works on Trailing Rule records through Storage without passing the Entity."""

    _entity = model.TrailingRule

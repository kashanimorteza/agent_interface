"""Entity Service Child for TrailingRule."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TrailingRule(BaseEntity[model.TrailingRule]):
    """The Child Service of the TrailingRule Entity."""

    _entity = model.TrailingRule

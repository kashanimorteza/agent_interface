"""Entity Service Child for PartialRule."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class PartialRule(BaseEntity[model.PartialRule]):
    """The Child Service of the PartialRule Entity."""

    _entity = model.PartialRule

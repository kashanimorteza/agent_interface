"""Entity Service Child for PartialGroup."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class PartialGroup(BaseEntity[model.PartialGroup]):
    """The Child Service of the PartialGroup Entity."""

    _entity = model.PartialGroup

"""Entity Service Child for TrailingGroup."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TrailingGroup(BaseEntity[model.TrailingGroup]):
    """The Child Service of the TrailingGroup Entity."""

    _entity = model.TrailingGroup

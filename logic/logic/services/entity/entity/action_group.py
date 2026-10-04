"""Entity Service Child for ActionGroup."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class ActionGroup(BaseEntity[model.ActionGroup]):
    """The Child Service of the ActionGroup Entity."""

    _entity = model.ActionGroup

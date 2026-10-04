"""Entity Service Child for Action."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Action(BaseEntity[model.Action]):
    """The Child Service of the Action Entity."""

    _entity = model.Action

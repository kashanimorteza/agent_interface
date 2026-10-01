"""Child Service of the Action Group Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class ActionGroup(BaseEntity):
    """The Entity Actions bound to the Action Group Entity."""

    _entity = model.ActionGroup

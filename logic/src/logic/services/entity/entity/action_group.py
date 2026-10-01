"""Child Service of the Action Group Entity."""

from model.interface import ActionGroup

from logic.services.entity.base_entity import BaseEntity


class ActionGroupService(BaseEntity):
    """The Entity Actions bound to the Action Group Entity."""

    _entity = ActionGroup

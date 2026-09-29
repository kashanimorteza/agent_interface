"""Entity Child Service bound to Model's Action Group Entity."""

from model.interface import ActionGroup

from logic.services.entity.base_entity import BaseEntity


class ActionGroupService(BaseEntity):
    """Selects Action Group once and offers every shared Entity Action for it."""

    entity = ActionGroup

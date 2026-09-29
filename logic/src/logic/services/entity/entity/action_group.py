"""Child Service for the ActionGroup Entity."""

from model.interface import ActionGroup

from logic.services.entity.base_entity import BaseEntity


class ActionGroupService(BaseEntity):
    """Entity-bound Actions for ActionGroup records."""

    entity = ActionGroup

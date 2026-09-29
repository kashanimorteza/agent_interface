"""The ActionGroup Service."""

from model.interface import ActionGroup

from logic.services.entity.base import EntityServiceBase


class ActionGroupService(EntityServiceBase[ActionGroup]):
    """Entity-bound Actions for ActionGroup records."""

    entity = ActionGroup

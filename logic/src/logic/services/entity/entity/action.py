"""Entity Child Service bound to Model's Action Entity."""

from model.interface import Action

from logic.services.entity.base_entity import BaseEntity


class ActionService(BaseEntity):
    """Selects Action once and offers every shared Entity Action for it."""

    entity = Action

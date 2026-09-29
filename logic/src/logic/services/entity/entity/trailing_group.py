"""Entity Child Service bound to Model's Trailing Group Entity."""

from model.interface import TrailingGroup

from logic.services.entity.base_entity import BaseEntity


class TrailingGroupService(BaseEntity):
    """Selects Trailing Group once and offers every shared Entity Action for it."""

    entity = TrailingGroup

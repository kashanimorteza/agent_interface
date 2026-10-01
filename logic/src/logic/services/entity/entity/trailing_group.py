"""Child Service of the Trailing Group Entity."""

from model.interface import TrailingGroup

from logic.services.entity.base_entity import BaseEntity


class TrailingGroupService(BaseEntity):
    """The Entity Actions bound to the Trailing Group Entity."""

    _entity = TrailingGroup

"""Child Service of the Trailing Group Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class TrailingGroup(BaseEntity):
    """The Entity Actions bound to the Trailing Group Entity."""

    _entity = model.TrailingGroup

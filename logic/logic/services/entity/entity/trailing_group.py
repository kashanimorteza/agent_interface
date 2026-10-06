"""The Trailing Group Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TrailingGroup(BaseEntity):
    """Child Service of the Trailing Group Entity."""

    _entity = model.TrailingGroup

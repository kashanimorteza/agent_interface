"""The TrailingGroup Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TrailingGroup(BaseEntity):
    """The Actions of the TrailingGroup Entity."""

    _entity = model.TrailingGroup

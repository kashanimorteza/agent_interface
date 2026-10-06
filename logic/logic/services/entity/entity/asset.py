"""The Asset Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Asset(BaseEntity):
    """The Actions of the Asset Entity."""

    _entity = model.Asset

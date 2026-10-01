"""Child Service of the Asset Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class Asset(BaseEntity):
    """The Entity Actions bound to the Asset Entity."""

    _entity = model.Asset

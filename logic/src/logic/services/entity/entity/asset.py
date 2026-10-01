"""Child Service of the Asset Entity."""

from model.interface import Asset

from logic.services.entity.base_entity import BaseEntity


class AssetService(BaseEntity):
    """The Entity Actions bound to the Asset Entity."""

    _entity = Asset

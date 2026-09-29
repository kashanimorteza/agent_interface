"""Child Service for the Asset Entity."""

from model.interface import Asset

from logic.services.entity.base_entity import BaseEntity


class AssetService(BaseEntity):
    """Entity-bound Actions for Asset records."""

    entity = Asset

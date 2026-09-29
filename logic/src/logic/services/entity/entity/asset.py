"""The Asset Service."""

from model.interface import Asset

from logic.services.entity.base import EntityServiceBase


class AssetService(EntityServiceBase[Asset]):
    """Entity-bound Actions for Asset records."""

    entity = Asset

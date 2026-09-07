"""Logic of the Asset Model."""

from my_model import Asset

from ..base import ModelLogic


class AssetLogic(ModelLogic[Asset]):
    model = Asset

from my_backend._model_interface import asset
from my_backend.logic._base import ModelLogic


class AssetLogic(ModelLogic[asset.Asset]):
    model_cls = asset.Asset

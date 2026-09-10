from __future__ import annotations

from my_model import Asset

from ._base import ModelLogic


class AssetLogic(ModelLogic[Asset]):
    model_cls = Asset

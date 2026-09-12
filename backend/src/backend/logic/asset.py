"""The Asset Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class AssetLogic(ModelLogic[m.Asset]):
    model_type = m.Asset

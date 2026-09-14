"""Asset Logic (task P3-G5-T3)."""

from __future__ import annotations

from ..model_interface import Asset
from .foundation import ModelLogicBase


class AssetLogic(ModelLogicBase[Asset]):
    model_cls = Asset

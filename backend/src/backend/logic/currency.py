"""Currency Logic (task P3-G5-T1)."""

from __future__ import annotations

from ..model_interface import Currency
from .foundation import ModelLogicBase


class CurrencyLogic(ModelLogicBase[Currency]):
    model_cls = Currency

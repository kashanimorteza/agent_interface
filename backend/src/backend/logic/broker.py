"""Broker Logic (task P3-G5-T2)."""

from __future__ import annotations

from ..model_interface import Broker
from .foundation import ModelLogicBase


class BrokerLogic(ModelLogicBase[Broker]):
    model_cls = Broker

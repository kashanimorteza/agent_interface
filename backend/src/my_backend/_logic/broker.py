from __future__ import annotations

from my_model import Broker

from ._base import ModelLogic


class BrokerLogic(ModelLogic[Broker]):
    model_cls = Broker

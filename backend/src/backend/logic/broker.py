"""The Broker Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class BrokerLogic(ModelLogic[m.Broker]):
    model_type = m.Broker

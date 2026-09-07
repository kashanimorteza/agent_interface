"""Logic of the Broker Model."""

from my_model import Broker

from ..base import ModelLogic


class BrokerLogic(ModelLogic[Broker]):
    model = Broker

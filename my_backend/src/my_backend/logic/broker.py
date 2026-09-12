from my_backend._model_interface import broker
from my_backend.logic._base import ModelLogic


class BrokerLogic(ModelLogic[broker.Broker]):
    model_cls = broker.Broker

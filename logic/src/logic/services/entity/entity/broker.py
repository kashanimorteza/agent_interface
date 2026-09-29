"""The Broker Service."""

from model.interface import Broker

from logic.services.entity.base import EntityServiceBase


class BrokerService(EntityServiceBase[Broker]):
    """Entity-bound Actions for Broker records."""

    entity = Broker

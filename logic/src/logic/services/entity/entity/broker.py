"""Child Service of the Broker Entity."""

from model.interface import Broker

from logic.services.entity.base_entity import BaseEntity


class BrokerService(BaseEntity):
    """The Entity Actions bound to the Broker Entity."""

    _entity = Broker

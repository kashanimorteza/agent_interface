"""Child Service for the Broker Entity."""

from model.interface import Broker

from logic.services.entity.base_entity import BaseEntity


class BrokerService(BaseEntity):
    """Entity-bound Actions for Broker records."""

    entity = Broker

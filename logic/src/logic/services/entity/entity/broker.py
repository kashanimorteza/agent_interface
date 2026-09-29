"""Entity Child Service bound to Model's Broker Entity."""

from model.interface import Broker

from logic.services.entity.base_entity import BaseEntity


class BrokerService(BaseEntity):
    """Selects Broker once and offers every shared Entity Action for it."""

    entity = Broker

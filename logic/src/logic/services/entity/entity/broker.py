"""Child Service of the Broker Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class Broker(BaseEntity):
    """The Entity Actions bound to the Broker Entity."""

    _entity = model.Broker

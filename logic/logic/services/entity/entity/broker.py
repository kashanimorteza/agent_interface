"""Entity Service Child for Broker."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Broker(BaseEntity[model.Broker]):
    """The Child Service of the Broker Entity."""

    _entity = model.Broker

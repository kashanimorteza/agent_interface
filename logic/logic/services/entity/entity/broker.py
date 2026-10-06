"""The Broker Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Broker(BaseEntity):
    """Child Service of the Broker Entity."""

    _entity = model.Broker

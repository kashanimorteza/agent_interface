"""The Broker Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Broker(BaseEntity):
    _entity = model.Broker

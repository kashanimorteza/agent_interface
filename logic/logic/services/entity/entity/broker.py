"""Broker: the Child Service bound to the Broker Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Broker(BaseEntity):
    """Works on Broker records through Storage without passing the Entity."""

    _entity = model.Broker

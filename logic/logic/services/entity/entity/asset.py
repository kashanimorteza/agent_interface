"""Asset: the Child Service bound to the Asset Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Asset(BaseEntity):
    """Works on Asset records through Storage without passing the Entity."""

    _entity = model.Asset

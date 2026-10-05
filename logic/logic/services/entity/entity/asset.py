from model import interface as model

from logic.services.entity.base import BaseEntity


class Asset(BaseEntity):
    _entity = model.Asset

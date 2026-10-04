"""Entity Service Child for Asset."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Asset(BaseEntity[model.Asset]):
    """The Child Service of the Asset Entity."""

    _entity = model.Asset

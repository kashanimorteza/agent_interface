"""Entity Service Child for Currency."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Currency(BaseEntity[model.Currency]):
    """The Child Service of the Currency Entity."""

    _entity = model.Currency

"""Entity Service Child for Account."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Account(BaseEntity[model.Account]):
    """The Child Service of the Account Entity."""

    _entity = model.Account

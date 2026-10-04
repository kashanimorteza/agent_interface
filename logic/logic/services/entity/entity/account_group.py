"""Entity Service Child for AccountGroup."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class AccountGroup(BaseEntity[model.AccountGroup]):
    """The Child Service of the AccountGroup Entity."""

    _entity = model.AccountGroup

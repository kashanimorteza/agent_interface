"""Child Service of the Account Group Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class AccountGroup(BaseEntity):
    """The Entity Actions bound to the Account Group Entity."""

    _entity = model.AccountGroup

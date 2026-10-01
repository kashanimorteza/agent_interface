"""Child Service of the Account Group Entity."""

from model.interface import AccountGroup

from logic.services.entity.base_entity import BaseEntity


class AccountGroupService(BaseEntity):
    """The Entity Actions bound to the Account Group Entity."""

    _entity = AccountGroup

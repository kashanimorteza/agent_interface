"""Child Service of the Account Entity."""

from model.interface import Account

from logic.services.entity.base_entity import BaseEntity


class AccountService(BaseEntity):
    """The Entity Actions bound to the Account Entity."""

    _entity = Account

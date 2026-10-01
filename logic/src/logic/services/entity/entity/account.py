"""Child Service of the Account Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class Account(BaseEntity):
    """The Entity Actions bound to the Account Entity."""

    _entity = model.Account

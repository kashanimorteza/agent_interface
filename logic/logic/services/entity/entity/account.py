"""The Account Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Account(BaseEntity):
    """Child Service of the Account Entity."""

    _entity = model.Account

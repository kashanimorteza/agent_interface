"""The Account Group Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class AccountGroup(BaseEntity):
    """Child Service of the Account Group Entity."""

    _entity = model.AccountGroup

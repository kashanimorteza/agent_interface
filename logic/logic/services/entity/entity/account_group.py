"""The AccountGroup Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class AccountGroup(BaseEntity):
    """The Actions of the AccountGroup Entity."""

    _entity = model.AccountGroup

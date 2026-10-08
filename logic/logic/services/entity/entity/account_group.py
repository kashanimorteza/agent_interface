"""AccountGroup: the Child Service bound to the Account Group Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class AccountGroup(BaseEntity):
    """Works on Account Group records through Storage without passing the Entity."""

    _entity = model.AccountGroup

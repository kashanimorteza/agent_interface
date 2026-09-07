"""Logic of the Account Group Model."""

from my_model import AccountGroup

from ..base import ModelLogic


class AccountGroupLogic(ModelLogic[AccountGroup]):
    model = AccountGroup

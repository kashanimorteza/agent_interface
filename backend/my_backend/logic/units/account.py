"""Logic of the Account Model."""

from my_model import Account

from ..base import ModelLogic


class AccountLogic(ModelLogic[Account]):
    model = Account

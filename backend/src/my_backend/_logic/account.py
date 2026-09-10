from __future__ import annotations

from my_model import Account

from ._base import ModelLogic


class AccountLogic(ModelLogic[Account]):
    model_cls = Account

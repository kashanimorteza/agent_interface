from __future__ import annotations

from my_model import AccountGroup

from ._base import ModelLogic


class AccountGroupLogic(ModelLogic[AccountGroup]):
    model_cls = AccountGroup

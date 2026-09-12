from my_backend._model_interface import account_group
from my_backend.logic._base import ModelLogic


class AccountGroupLogic(ModelLogic[account_group.AccountGroup]):
    model_cls = account_group.AccountGroup

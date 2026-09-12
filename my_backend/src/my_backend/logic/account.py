from my_backend._model_interface import account
from my_backend.logic._base import ModelLogic


class AccountLogic(ModelLogic[account.Account]):
    model_cls = account.Account

from my_backend._model_interface import user
from my_backend.logic._base import ModelLogic


class UserLogic(ModelLogic[user.User]):
    model_cls = user.User

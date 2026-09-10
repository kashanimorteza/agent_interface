from __future__ import annotations

from my_model import User

from ._base import ModelLogic


class UserLogic(ModelLogic[User]):
    model_cls = User

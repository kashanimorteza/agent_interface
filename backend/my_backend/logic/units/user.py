"""Logic of the User Model."""

from my_model import User

from ..base import ModelLogic


class UserLogic(ModelLogic[User]):
    model = User

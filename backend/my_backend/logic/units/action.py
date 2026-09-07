"""Logic of the Action Model."""

from my_model import Action

from ..base import ModelLogic


class ActionLogic(ModelLogic[Action]):
    model = Action

"""Logic of the Action Group Model."""

from my_model import ActionGroup

from ..base import ModelLogic


class ActionGroupLogic(ModelLogic[ActionGroup]):
    model = ActionGroup

"""The User Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class UserLogic(ModelLogic[m.User]):
    model_type = m.User

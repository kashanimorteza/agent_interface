"""The Account Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class AccountLogic(ModelLogic[m.Account]):
    model_type = m.Account

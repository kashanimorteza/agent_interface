"""The Account Group Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class AccountGroupLogic(ModelLogic[m.AccountGroup]):
    model_type = m.AccountGroup

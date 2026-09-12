"""The Instance Model's Logic unit."""

from __future__ import annotations

import my_model as m

from ._base import ModelLogic


class InstanceLogic(ModelLogic[m.Instance]):
    model_type = m.Instance

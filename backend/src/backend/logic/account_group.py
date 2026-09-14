"""Account Group Logic (task P3-G6-T1)."""

from __future__ import annotations

from ..model_interface import AccountGroup
from .foundation import ModelLogicBase


class AccountGroupLogic(ModelLogicBase[AccountGroup]):
    model_cls = AccountGroup

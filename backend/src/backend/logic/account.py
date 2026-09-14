"""Account Logic (task P3-G6-T2)."""

from __future__ import annotations

from ..model_interface import Account
from .foundation import ModelLogicBase


class AccountLogic(ModelLogicBase[Account]):
    model_cls = Account

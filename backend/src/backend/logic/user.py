"""User Logic (task P3-G4-T1)."""

from __future__ import annotations

from ..model_interface import User
from .foundation import ModelLogicBase


class UserLogic(ModelLogicBase[User]):
    model_cls = User

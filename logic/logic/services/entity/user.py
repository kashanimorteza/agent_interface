"""The User Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class User(BaseEntity):
    """The Actions of the User Entity."""

    _entity = model.User

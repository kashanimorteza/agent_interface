"""Child Service of the User Entity."""

from model import interface as model

from logic.services.entity.base_entity import BaseEntity


class User(BaseEntity):
    """The Entity Actions bound to the User Entity."""

    _entity = model.User

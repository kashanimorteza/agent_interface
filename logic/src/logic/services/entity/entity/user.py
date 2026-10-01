"""Child Service of the User Entity."""

from model.interface import User

from logic.services.entity.base_entity import BaseEntity


class UserService(BaseEntity):
    """The Entity Actions bound to the User Entity."""

    _entity = User

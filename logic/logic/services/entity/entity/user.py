"""User: the Child Service bound to the User Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class User(BaseEntity):
    """Works on User records through Storage without passing the Entity."""

    _entity = model.User

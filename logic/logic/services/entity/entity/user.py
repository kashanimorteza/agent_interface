from model import interface as model

from logic.services.entity.base import BaseEntity


class User(BaseEntity):
    _entity = model.User

from model import interface as model

from logic.services.entity.base import BaseEntity


class Account(BaseEntity):
    _entity = model.Account

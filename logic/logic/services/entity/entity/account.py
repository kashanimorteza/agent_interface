"""Account: the Child Service bound to the Account Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Account(BaseEntity):
    """Works on Account records through Storage without passing the Entity."""

    _entity = model.Account

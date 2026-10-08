"""TrailingGroup: the Child Service bound to the Trailing Group Entity."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TrailingGroup(BaseEntity):
    """Works on Trailing Group records through Storage without passing the Entity."""

    _entity = model.TrailingGroup

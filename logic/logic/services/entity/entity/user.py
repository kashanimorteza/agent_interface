"""Entity Service Child for User."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class User(BaseEntity[model.User]):
    """The Child Service of the User Entity."""

    _entity = model.User

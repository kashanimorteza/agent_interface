"""Entity Service Child for Instance."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class Instance(BaseEntity[model.Instance]):
    """The Child Service of the Instance Entity."""

    _entity = model.Instance

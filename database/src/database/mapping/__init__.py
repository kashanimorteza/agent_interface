from model.foundation import ModelBase

from ..foundation import StorageBase

MAPPINGS: dict[type[ModelBase], type[StorageBase]] = {}


def register(model_type: type[ModelBase]):
    def decorator(orm_cls: type[StorageBase]) -> type[StorageBase]:
        MAPPINGS[model_type] = orm_cls
        return orm_cls

    return decorator


from . import accounts, actions, identity, reference, risk

__all__ = ["MAPPINGS", "accounts", "actions", "identity", "reference", "risk"]

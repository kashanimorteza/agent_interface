"""API dependencies: the Data Access boundary and the Logic unit of one Model."""

from collections.abc import Callable
from typing import Annotated

from fastapi import Depends

from trading_backend.data_access.database import DataAccess, get_data_access
from trading_backend.logic.model_logic import ModelLogic
from trading_backend.logic.models import get_logic

DataAccessDep = Annotated[DataAccess, Depends(get_data_access)]


def logic_dependency(model: str) -> Callable[..., ModelLogic]:
    """A dependency that builds the Logic unit of ``model`` on the application's Data Access."""

    def provide(data_access: DataAccessDep) -> ModelLogic:
        return get_logic(model, data_access)

    provide.__name__ = f"provide_{model}_logic"
    return provide

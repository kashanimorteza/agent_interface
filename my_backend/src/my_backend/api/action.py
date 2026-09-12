from my_backend._model_interface import action
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.action import ActionLogic

_Read, _Create, _Update = build_schemas(action.Action)

router = build_router(
    name="Action",
    logic_cls=ActionLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/actions",
    has_status=True,
)

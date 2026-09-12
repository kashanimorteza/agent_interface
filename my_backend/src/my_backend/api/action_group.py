from my_backend._model_interface import action_group
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.action_group import ActionGroupLogic

_Read, _Create, _Update = build_schemas(action_group.ActionGroup)

router = build_router(
    name="ActionGroup",
    logic_cls=ActionGroupLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/action-groups",
    has_status=True,
)

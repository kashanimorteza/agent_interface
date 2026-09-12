from my_backend._model_interface import trailing_group
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.trailing_group import TrailingGroupLogic

_Read, _Create, _Update = build_schemas(trailing_group.TrailingGroup)

router = build_router(
    name="TrailingGroup",
    logic_cls=TrailingGroupLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/trailing-groups",
    has_status=True,
)

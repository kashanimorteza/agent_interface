from my_backend._model_interface import position
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.position import PositionLogic

_Read, _Create, _Update = build_schemas(position.Position)

router = build_router(
    name="Position",
    logic_cls=PositionLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/positions",
    has_status=True,
)

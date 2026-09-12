from my_backend._model_interface import user
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.user import UserLogic

_Read, _Create, _Update = build_schemas(user.User)

router = build_router(
    name="User",
    logic_cls=UserLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/users",
    has_status=True,
)

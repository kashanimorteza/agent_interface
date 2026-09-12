from my_backend._model_interface import instance
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.instance import InstanceLogic

_Read, _Create, _Update = build_schemas(instance.Instance)

router = build_router(
    name="Instance",
    logic_cls=InstanceLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/instances",
    has_status=True,
)

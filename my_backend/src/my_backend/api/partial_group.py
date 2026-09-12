from my_backend._model_interface import partial_group
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.partial_group import PartialGroupLogic

_Read, _Create, _Update = build_schemas(partial_group.PartialGroup)

router = build_router(
    name="PartialGroup",
    logic_cls=PartialGroupLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/partial-groups",
    has_status=True,
)

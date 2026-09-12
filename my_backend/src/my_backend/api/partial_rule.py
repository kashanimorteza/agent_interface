from my_backend._model_interface import partial_rule
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.partial_rule import PartialRuleLogic

_Read, _Create, _Update = build_schemas(partial_rule.PartialRule)

router = build_router(
    name="PartialRule",
    logic_cls=PartialRuleLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/partial-rules",
    has_status=True,
)

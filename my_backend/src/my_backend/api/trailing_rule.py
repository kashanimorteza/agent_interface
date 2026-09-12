from my_backend._model_interface import trailing_rule
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.trailing_rule import TrailingRuleLogic

_Read, _Create, _Update = build_schemas(trailing_rule.TrailingRule)

router = build_router(
    name="TrailingRule",
    logic_cls=TrailingRuleLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/trailing-rules",
    has_status=True,
)

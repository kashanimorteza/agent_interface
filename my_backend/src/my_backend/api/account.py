from my_backend._model_interface import account
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.account import AccountLogic

_Read, _Create, _Update = build_schemas(account.Account)

router = build_router(
    name="Account",
    logic_cls=AccountLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/accounts",
    has_status=True,
)

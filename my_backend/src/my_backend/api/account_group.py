from my_backend._model_interface import account_group
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.account_group import AccountGroupLogic

_Read, _Create, _Update = build_schemas(account_group.AccountGroup)

router = build_router(
    name="AccountGroup",
    logic_cls=AccountGroupLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/account-groups",
    has_status=True,
)

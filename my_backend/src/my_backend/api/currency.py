from my_backend._model_interface import currency
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.currency import CurrencyLogic

_Read, _Create, _Update = build_schemas(currency.Currency)

router = build_router(
    name="Currency",
    logic_cls=CurrencyLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/currencies",
    has_status=True,
)

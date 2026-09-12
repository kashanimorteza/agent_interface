from my_backend._model_interface import trading_platform
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.trading_platform import TradingPlatformLogic

_Read, _Create, _Update = build_schemas(trading_platform.TradingPlatform)

router = build_router(
    name="TradingPlatform",
    logic_cls=TradingPlatformLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/trading-platforms",
    has_status=True,
)

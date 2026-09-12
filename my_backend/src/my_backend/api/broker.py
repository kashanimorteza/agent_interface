from my_backend._model_interface import broker
from my_backend._schemas import build_schemas
from my_backend.api._factory import build_router
from my_backend.logic.broker import BrokerLogic

_Read, _Create, _Update = build_schemas(broker.Broker)

router = build_router(
    name="Broker",
    logic_cls=BrokerLogic,
    read_schema=_Read,
    create_schema=_Create,
    update_schema=_Update,
    prefix="/brokers",
    has_status=True,
)

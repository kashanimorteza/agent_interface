from my_model._declarations import AwaitingGeneration, GenerationMethod
from my_model._models.instance import Instance

RECORDS: tuple[Instance, ...] = (
    Instance(
        name="FxPro MetaTrader",
        broker_id=1,
        trading_platform_id=1,
        ip="127.0.0.1",
        username="test",
        password=AwaitingGeneration(GenerationMethod.SECURE),
        api_key=AwaitingGeneration(GenerationMethod.SECURE),
    ),
)

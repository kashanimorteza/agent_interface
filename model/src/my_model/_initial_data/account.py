from my_model._declarations import AwaitingGeneration, GenerationMethod
from my_model._models.account import Account

RECORDS: tuple[Account, ...] = (
    Account(
        name="Acc-1",
        group_id=1,
        broker_id=1,
        instance_id=1,
        base_currency_id=1,
        username="test",
        password=AwaitingGeneration(GenerationMethod.SECURE),
        leverage=100,
        account_type="CFD",
    ),
)

"""A supported trading API standard."""

from ..foundation import FieldSpec, FieldType, InitialRecord, define_entity

TradingPlatform = define_entity(
    name="TradingPlatform",
    purpose=(
        "A supported trading API standard, such as MetaTrader 5 or Binance. The "
        "platform is carried as domain data naming the implementation the "
        "application is to use, which is what keeps the system independent of any "
        "one exchange or broker."
    ),
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The platform's display name."),
        "code": FieldSpec(
            type=FieldType.STRING,
            nullable=False,
            purpose=(
                "Identifies the implementation the application must use for this "
                "platform, such as binance or metatrader_5."
            ),
        ),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the platform."),
    },
    initial_records=[
        InitialRecord({"name": "MetaTrader 5", "code": "metatrader_5"}),
        InitialRecord({"name": "Binance", "code": "binance"}),
    ],
)

"""Something that can be selected for trading."""

from ..foundation import FieldSpec, FieldType, InitialRecord, define_entity

Asset = define_entity(
    name="Asset",
    purpose=(
        "An asset that can be traded, carrying the category it belongs to and the "
        "values that describe how its price is expressed, so the system knows "
        "exactly what is being traded and how finely it moves."
    ),
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The asset's display name."),
        "symbol": FieldSpec(
            type=FieldType.STRING,
            nullable=False,
            unique=True,
            purpose="Identifies the tradable asset, such as EUR/USD, XAU/USD or USOil.",
        ),
        "category": FieldSpec(
            type=FieldType.STRING,
            nullable=False,
            purpose="The asset category, such as Currency, Commodity or Cryptocurrency.",
        ),
        "point_size": FieldSpec(
            type=FieldType.FLOAT,
            nullable=False,
            default=0.0,
            purpose="The size of one point for the asset.",
        ),
        "digits": FieldSpec(
            type=FieldType.INTEGER,
            nullable=False,
            default=0,
            purpose="The number of decimal digits used for the asset's price.",
        ),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the asset."),
    },
    initial_records=[
        InitialRecord({"name": "EURUSD", "symbol": "EUR/USD", "category": "Currency", "point_size": 0.0001, "digits": 5}),
        InitialRecord({"name": "EURGBP", "symbol": "EUR/GBP", "category": "Currency", "point_size": 0.001, "digits": 5}),
        InitialRecord({"name": "XAUUSD", "symbol": "XAU/USD", "category": "Commodity", "point_size": 0.01, "digits": 2}),
        InitialRecord({"name": "USOil", "symbol": "USOil", "category": "Commodity", "point_size": 0.01, "digits": 3}),
    ],
)

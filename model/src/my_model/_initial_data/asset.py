from my_model._models.asset import Asset

RECORDS: tuple[Asset, ...] = (
    Asset(broker_id=1, name="EURUSD", symbol="EUR/USD", category="Currency", point_size=0.0001, digits=5),
    Asset(broker_id=1, name="EURGBP", symbol="EUR/GBP", category="Currency", point_size=0.001, digits=5),
    Asset(broker_id=1, name="XAUUSD", symbol="XAU/USD", category="Commodity", point_size=0.01, digits=2),
    Asset(broker_id=1, name="USOil", symbol="USOil", category="Commodity", point_size=0.01, digits=3),
)

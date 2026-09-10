from my_model._models.trading_platform import TradingPlatform

RECORDS: tuple[TradingPlatform, ...] = (
    TradingPlatform(name="MetaTrader 5", code="metatrader_5"),
    TradingPlatform(name="Binance", code="binance"),
)

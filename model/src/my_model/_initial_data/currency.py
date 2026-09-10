from my_model._models.currency import Currency

RECORDS: tuple[Currency, ...] = (
    Currency(user_id=1, name="US Dollar", code="USD", symbol="$", country="United States", decimal_digits=2),
    Currency(user_id=1, name="Euro", code="EUR", symbol="€", country="Eurozone", decimal_digits=2),
    Currency(user_id=1, name="British Pound", code="GBP", symbol="£", country="United Kingdom", decimal_digits=2),
    Currency(user_id=1, name="Japanese Yen", code="JPY", symbol="¥", country="Japan", decimal_digits=0),
    Currency(user_id=1, name="Swiss Franc", code="CHF", symbol="CHF", country="Switzerland", decimal_digits=2),
    Currency(user_id=1, name="Canadian Dollar", code="CAD", symbol="C$", country="Canada", decimal_digits=2),
    Currency(user_id=1, name="Australian Dollar", code="AUD", symbol="A$", country="Australia", decimal_digits=2),
    Currency(user_id=1, name="New Zealand Dollar", code="NZD", symbol="NZ$", country="New Zealand", decimal_digits=2),
)

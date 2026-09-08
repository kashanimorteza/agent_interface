"""A currency the trading system can work in."""

from ..foundation import (
    DomainRule,
    FieldSpec,
    FieldType,
    InitialRecord,
    RuleScope,
    define_entity,
)

CODE_LENGTH = 3


def _code_is_exactly_the_declared_length(currency) -> str | None:
    if currency.code is not None and len(currency.code) != CODE_LENGTH:
        return f"{currency.code!r} is {len(currency.code)} characters"
    return None


Currency = define_entity(
    name="Currency",
    purpose=(
        "A currency the trading system can use, identified by its standard code "
        "and carrying the decimal precision its monetary values are held at."
    ),
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The currency's full name."),
        "code": FieldSpec(
            type=FieldType.STRING,
            size=CODE_LENGTH,
            nullable=False,
            unique=True,
            purpose="The currency's standard three-letter code, such as USD or EUR.",
        ),
        "symbol": FieldSpec(
            type=FieldType.STRING,
            nullable=True,
            purpose="The currency's display symbol, such as $, € or £.",
        ),
        "country": FieldSpec(
            type=FieldType.STRING,
            nullable=True,
            purpose="The country or region associated with the currency.",
        ),
        "decimal_digits": FieldSpec(
            type=FieldType.INTEGER,
            nullable=False,
            default=2,
            purpose="The number of decimal digits monetary values normally use.",
        ),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the currency."),
    },
    rules=[
        DomainRule(
            statement="The standard code is exactly three characters long.",
            scope=RuleScope.OWN_DATA,
            fields=("code",),
            check=_code_is_exactly_the_declared_length,
        ),
    ],
    initial_records=[
        InitialRecord({"name": "US Dollar", "code": "USD", "symbol": "$", "country": "United States", "decimal_digits": 2}),
        InitialRecord({"name": "Euro", "code": "EUR", "symbol": "€", "country": "Eurozone", "decimal_digits": 2}),
        InitialRecord({"name": "British Pound", "code": "GBP", "symbol": "£", "country": "United Kingdom", "decimal_digits": 2}),
        InitialRecord({"name": "Japanese Yen", "code": "JPY", "symbol": "¥", "country": "Japan", "decimal_digits": 0}),
        InitialRecord({"name": "Swiss Franc", "code": "CHF", "symbol": "CHF", "country": "Switzerland", "decimal_digits": 2}),
        InitialRecord({"name": "Canadian Dollar", "code": "CAD", "symbol": "C$", "country": "Canada", "decimal_digits": 2}),
        InitialRecord({"name": "Australian Dollar", "code": "AUD", "symbol": "A$", "country": "Australia", "decimal_digits": 2}),
        InitialRecord({"name": "New Zealand Dollar", "code": "NZD", "symbol": "NZ$", "country": "New Zealand", "decimal_digits": 2}),
    ],
)

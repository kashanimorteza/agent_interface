"""Declared Initial Data and the coordination that inserts it into an Instance."""

from collections.abc import Mapping, Sequence
from decimal import Decimal
from typing import Any

from database.core import statements
from database.core.credentials import Credentials


class Credential:
    """Marker for a value that is generated securely when the record is inserted."""


CREDENTIAL = Credential()

DECLARED: dict[str, list[dict[str, Any]]] = {
    "User": [
        {
            "name": "Admin",
            "username": "admin",
            "password": CREDENTIAL,
            "api_key": CREDENTIAL,
        },
    ],
    "Trading Platform": [
        {"name": "MetaTrader 5", "code": "metatrader_5"},
        {"name": "Binance", "code": "binance"},
    ],
    "Instance": [
        {
            "name": "MetaTrader",
            "user_id": 1,
            "trading_platform_id": 1,
            "ip": "127.0.0.1",
            "username": "test",
            "password": CREDENTIAL,
            "api_key": CREDENTIAL,
        },
    ],
    "Currency": [
        {
            "user_id": 1,
            "code": "USD",
            "symbol": "$",
            "country": "United States",
            "decimal_digits": 2,
        },
        {
            "user_id": 1,
            "code": "EUR",
            "symbol": "€",
            "country": "Eurozone",
            "decimal_digits": 2,
        },
        {
            "user_id": 1,
            "code": "GBP",
            "symbol": "£",
            "country": "United Kingdom",
            "decimal_digits": 2,
        },
        {
            "user_id": 1,
            "code": "JPY",
            "symbol": "¥",
            "country": "Japan",
            "decimal_digits": 0,
        },
        {
            "user_id": 1,
            "code": "CHF",
            "symbol": "CHF",
            "country": "Switzerland",
            "decimal_digits": 2,
        },
        {
            "user_id": 1,
            "code": "CAD",
            "symbol": "C$",
            "country": "Canada",
            "decimal_digits": 2,
        },
        {
            "user_id": 1,
            "code": "AUD",
            "symbol": "A$",
            "country": "Australia",
            "decimal_digits": 2,
        },
        {
            "user_id": 1,
            "code": "NZD",
            "symbol": "NZ$",
            "country": "New Zealand",
            "decimal_digits": 2,
        },
    ],
    "Broker": [{"name": "FxPro", "user_id": 1}],
    "Asset": [
        {
            "broker_id": 1,
            "symbol": "EUR/USD",
            "category": "Currency",
            "point_size": 0.0001,
            "digits": 5,
        },
        {
            "broker_id": 1,
            "symbol": "EUR/GBP",
            "category": "Currency",
            "point_size": 0.001,
            "digits": 5,
        },
        {
            "broker_id": 1,
            "symbol": "XAU/USD",
            "category": "Commodity",
            "point_size": 0.01,
            "digits": 2,
        },
        {
            "broker_id": 1,
            "symbol": "USOil",
            "category": "Commodity",
            "point_size": 0.01,
            "digits": 3,
        },
    ],
    "Account Group": [{"user_id": 1, "name": "Default"}],
    "Account": [
        {
            "name": "Acc-1",
            "group_id": 1,
            "broker_id": 1,
            "instance_id": 1,
            "base_currency_id": 1,
            "username": "test",
            "password": CREDENTIAL,
            "leverage": 100,
            "account_type": "CFD",
        },
    ],
    "Trailing Group": [{"user_id": 1, "name": "Default"}],
    "Partial Group": [{"user_id": 1, "name": "Default"}],
    "Action Group": [{"user_id": 1, "name": "Default"}],
    "Action": [
        {
            "name": "Default",
            "action_group_id": 1,
            "asset_id": 1,
            "account_id": 1,
            "partial_group_id": 1,
            "trailing_group_id": 1,
            "risk_by_reward": Decimal(1),
            "take_profit": Decimal(1),
            "stop_loss": Decimal(1),
        },
    ],
}


def insert_initial_data(
    instance: Any,
    entities: Sequence[Any],
    declared: Mapping[str, Sequence[Mapping[str, Any]]] = DECLARED,
) -> int:
    """Insert every declared record that the Instance does not already hold.

    The records are processed in Entity order in one atomic change. A declared reference
    names the position of a declared record and resolves to the stored id of that record.
    A record is already held when a Uniqueness Constraint of its Entity is satisfied by a
    stored record.

    Args:
        instance (Any): Instance implementation whose Tables exist.
        entities (Sequence[Any]): Entity classes in Target order.
        declared (Mapping): Declared records by Entity name.

    Returns:
        (int): Number of records inserted.
    """
    credentials = Credentials()
    stored_ids: dict[str, list[int]] = {}
    inserted = 0
    with instance.transaction() as transaction:
        for entity in entities:
            declaration = entity.declaration
            for record in declared.get(declaration.name, ()):
                values = _resolve_references(declaration, record, stored_ids)
                stored = _held(transaction, entity, values)
                if stored is None:
                    generated = {
                        name: credentials.next() if value is CREDENTIAL else value
                        for name, value in values.items()
                    }
                    stored = transaction.insert(
                        entity, statements.values_of(entity(**generated))
                    )
                    inserted += 1
                stored_ids.setdefault(declaration.name, []).append(
                    stored[declaration.primary_key]
                )
    return inserted


def _resolve_references(
    declaration: Any, record: Mapping[str, Any], stored_ids: Mapping[str, list[int]]
) -> dict[str, Any]:
    values = dict(record)
    for relation in declaration.relations:
        if relation.local_field in values and relation.target_entity in stored_ids:
            position = values[relation.local_field] - 1
            values[relation.local_field] = stored_ids[relation.target_entity][position]
    return values


def _held(
    transaction: statements.Transaction, entity: Any, values: Mapping[str, Any]
) -> dict[str, Any] | None:
    for constraint in entity.declaration.unique_constraints:
        if all(name in values for name in constraint.fields):
            found = transaction.find(entity, values, constraint.fields)
            if found is not None:
                return found
    return None

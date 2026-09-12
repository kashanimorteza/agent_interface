# my_model

The independent, platform-independent logical Model for the Trading Assistant. It defines the domain entities, their fields, relationships, and rules, and gives every other technical component (Database, Backend, Frontend) one shared understanding of the project's data.

## Purpose and boundaries

`my_model` owns domain representations, field semantics, conceptual relationships, domain rules that are determinable from a single record's own data, initial-data declarations, and one stable public package interface.

It does **not** own persistence (tables, columns, ORM mappings, queries, migrations), HTTP/API transport, business workflows, or presentation. Cross-record rules — such as "no two records may share the same name" — are declared here (see [Uniqueness rules](#uniqueness-rules)) but enforced by Database, since only Database has access to every persisted record.

## Installation and import

The package is managed with [uv](https://docs.astral.sh/uv/) and targets Python 3.13+.

```bash
cd my_model
uv sync
```

Two equivalent import styles are supported:

```python
import my_model

my_model.user.User(name="Ada", username="ada", password="...", api_key="...")
```

```python
from my_model import user

user.User(name="Ada", username="ada", password="...", api_key="...")
```

A Model is always identified by its imported type — never by a string name.

## Public interface

`my_model.__all__` lists every public domain module: `user`, `trading_platform`, `instance`, `currency`, `broker`, `asset`, `account_group`, `account`, `trailing_group`, `trailing_rule`, `partial_group`, `partial_rule`, `action_group`, `action`, `position`. Each module exposes exactly one Pydantic model class (e.g. `user.User`).

Internal modules (`my_model._base`, `my_model._unique`, `my_model._initial_data`) are implementation details and are not part of the supported interface.

## Domain entities

| Model | Represents | Belongs to / Uses |
| --- | --- | --- |
| `User` | An independent user of the system. | — |
| `TradingPlatform` | A supported trading API standard (e.g. MetaTrader 5, Binance). | — |
| `Instance` | A user's connection to a Trading Platform. | User, Trading Platform |
| `Currency` | A currency usable by the trading system. | User |
| `Broker` | A broker supported by the system. | User |
| `Asset` | A tradable asset offered by a Broker. | Broker |
| `AccountGroup` | A group organizing a user's trading accounts. | User |
| `Account` | A funded trading account. | Account Group, Broker, Instance, Currency |
| `TrailingGroup` | A group of Stop Loss / Take Profit rules. | User |
| `TrailingRule` | One activation rule within a Trailing Group. | Trailing Group |
| `PartialGroup` | A group of partial-close rules. | User |
| `PartialRule` | One activation rule within a Partial Group. | Partial Group |
| `ActionGroup` | A risk-profile grouping for Actions. | User |
| `Action` | How a position must be opened. | Action Group, Asset, Account, Partial Group, Trailing Group |
| `Position` | The complete record of a created position. | User, Trading Platform, Broker, Account, Trailing Group, Partial Group, Action Group, Action |

Relationships are represented as plain integer reference fields (e.g. `user_id`) — no ORM relationship objects live in this package.

## Constructing a valid instance

```python
from my_model.broker import Broker

broker = Broker(name="Example Broker", user_id=1)
```

Every field's required/optional, nullable, and default behavior matches the project's Model definition exactly. Omitting a required field raises `pydantic.ValidationError`:

```python
from pydantic import ValidationError
from my_model.broker import Broker

try:
    Broker(user_id=1)  # missing required "name"
except ValidationError as exc:
    print(exc)
```

Unknown fields are rejected (closed domain objects):

```python
Broker(name="Example", user_id=1, unexpected="value")  # raises ValidationError
```

## Serialization and schema

```python
from my_model.broker import Broker

broker = Broker(name="Example Broker", user_id=1)
data = broker.model_dump()
restored = Broker.model_validate(data)
schema = Broker.model_json_schema()
```

`model_dump_json()` is available the same way for JSON output.

## Credential and sensitive fields

A field that carries a credential (e.g. `User.password`, `User.api_key`, `Instance.password`, `Account.password`) is marked in its JSON schema with `credential: true` and, where the Target specifies a storage expectation, `storage_at_rest` (`"hash"` or `"encrypted"`). Credential fields are excluded from `repr()` output:

```python
from my_model.user import User

u = User(name="Ada", username="ada", password="secret", api_key="key")
print(repr(u))  # password and api_key are never shown
print(User.model_json_schema()["properties"]["password"]["credential"])  # True
```

`my_model` never decides *how* a credential is hashed or encrypted — that implementation belongs to Database. It only declares which fields are sensitive and what the domain expects.

## Uniqueness rules

A Model that participates in a cross-record uniqueness rule declares it on a `UNIQUE_TOGETHER` class attribute — a tuple of field-name tuples:

```python
from my_model.currency import Currency

Currency.UNIQUE_TOGETHER  # (("user_id", "code"),)
```

`my_model._unique` provides a pure, side-effect-free way to compare two already-loaded records against such a rule; it performs no lookup of its own:

```python
from my_model._unique import find_colliding_record
from my_model.currency import Currency

existing = [Currency(user_id=1, code="USD")]
candidate = Currency(user_id=1, code="USD")
found = find_colliding_record(candidate, existing, ("user_id", "code"))
found  # -> the matching record
```

Proving uniqueness across *all persisted* records is Database's responsibility; this package only carries the rule and a way to apply it to records already in hand.

## Initial data

A Model with Target-required seed records declares them on an `INITIAL_DATA` class attribute — a tuple of plain dictionaries, never inserted by this package:

```python
from my_model.trading_platform import TradingPlatform

TradingPlatform.INITIAL_DATA
# ({"name": "MetaTrader 5", "code": "metatrader_5"}, {"name": "Binance", "code": "binance"})
```

A field the Target marks "generate securely" (such as a seeded user's password) carries the `my_model._initial_data.GENERATE_SECURELY` sentinel instead of a literal value — this package never fabricates or stores a placeholder secret. Database resolves that sentinel to an actual generated value at insertion time.

## Partial updates: omitted vs. explicit `None`

Every optional field distinguishes "not supplied" from "explicitly cleared":

```python
from my_model.currency import Currency

c = Currency(user_id=1, code="USD")
c.symbol  # None (field default, not supplied)

update = {"symbol": None}  # explicit clear
merged = c.model_copy(update=update)
merged.symbol  # None (explicitly set)
```

## Domain-specific behavior

`Instance.missing_required_connection_fields(required_fields)` reports which platform-required connection fields (e.g. `ip`, `username`) are absent from a given Instance — a deterministic check over the Instance's own data, with no knowledge of persisted state.

## Dependencies

- [pydantic](https://docs.pydantic.dev/) `2.x` — the only runtime dependency.
- Development-only: `ruff` (lint/format), `pyright` (type checking), `pytest` (tests).

## Configuration

None. The package has no environment variables or runtime configuration; every behavior is expressed through its Python API.

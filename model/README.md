# Model

## Overview

**What it is.** The Model Component is the Trading Assistant's shared domain vocabulary: one authoritative
*Domain Definition* for every concept the Target defines — users, trading platforms, instances, currencies,
brokers, assets, accounts, trailing and partial rule groups, actions, and positions.

**What it does.** Each Domain Definition states its Fields, their rules, and its relationships once, validates
data against them, and converts to and from a *Plain Representation* (simple named values) that any consumer
can encode as JSON. Every definition also *declares itself* — its Fields, uniqueness, credentials, and
relationships — so other Components read the same meaning instead of redefining it.

**Where it sits.** Model is a library. Database, Logic, API, and Presentation consume it through its Public
Interface. Model stores nothing, performs no application behaviour, and offers no stored-data operations
(no saving, loading, listing, or deleting). It does not own initial data.

## Interface

Everything is published by one import, `model`. Its public names are exactly the fifteen Domain Definitions
below, and every one offers the same three Operations.

```text
model
├── User · TradingPlatform · Instance · Currency · Broker · Asset · AccountGroup · Account
│   TrailingGroup · TrailingRule · PartialGroup · PartialRule · ActionGroup · Action · Position
│   ├── Conversion
│   │   ├── deserialize(data) -> definition
│   │   └── serialize() -> dict
│   └── Declaration
│       └── declaration() -> declaration
```

### Operations

| Category | Operation | Accepts | Returns | Outcomes |
|---|---|---|---|---|
| Conversion | `Definition.deserialize(data)` | A mapping of Field names to values (a Plain Representation). | A new, validated instance of the definition. | Succeeds when every rule holds. Otherwise raises `pydantic.ValidationError` whose errors name each offending Field: an unknown key, a missing required Field, a null in a Field that is not optional, a value of the wrong kind, or a value that breaks a Field's own rule are all rejected. |
| Conversion | `instance.serialize()` | Nothing. | A dictionary with one entry per Field, in declaration order. Values are JSON-compatible: exact decimals and instants appear as text, and a relationship appears only as its reference value (for example `user_id`), never as a nested record. No Field is withheld, credentials included; deciding what leaves an API is the consumer's job. | Always succeeds for a valid instance. |
| Declaration | `Definition.declaration()` | Nothing. | A declaration with `name`, `persistence`, `fields`, `identity`, `unique_sets`, and `relationships`. Each entry of `fields` has `name`, `type`, `length`, `precision`, `optional`, `has_default`, `default`, `identity`, `generated`, `unique`, `credential` (the at-rest treatment or `None`), and `activation`. Each entry of `relationships` has `field`, `definition` (the referenced definition itself), `referenced_field`, `cardinality`, and `optional`. | Always succeeds. |

A definition can also be built directly with keyword arguments, for example `User(name="Admin", ...)`; the same
rules apply.

Rules that hold for every definition:

* A record's `id` is *generated*: something else produces it, so it is absent (`None`) until then. It is never
  null once produced and is not something the domain supplies.
* Text values are trimmed of surrounding whitespace when validated.
* Validation is strict: a value of the wrong kind (a text `"7"` for an integer, a text `"yes"` for a boolean) is
  rejected rather than converted. Exact decimals and instants are given as text or as `Decimal`/`datetime`.
* Exact decimals never lose precision; a fractional balance survives a round trip unchanged.
* Every definition is `persistent`, and every definition has an activation Field, `is_active`, that defaults to
  `True`.

### Example: read a declaration

```python
from model import Account

declaration = Account.declaration()
print(declaration.persistence.value)
# -> persistent
print([(r.field, r.definition.__name__) for r in declaration.relationships])
# -> [('group_id', 'AccountGroup'), ('broker_id', 'Broker'), ('instance_id', 'Instance'), ('base_currency_id', 'Currency')]
print(declaration.unique_sets)
# -> (('group_id', 'broker_id', 'instance_id'),)
```

### Example: reject invalid data

```python
from pydantic import ValidationError

from model import Currency

try:
    Currency.deserialize({"user_id": 1, "code": "US"})
except ValidationError as error:
    print(sorted({str(item["loc"][0]) for item in error.errors()}))
# -> ['code']
```

### Domain Definitions

#### Account

A funded trading account through which the system executes trades and launches positions.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `name` | string | required; unique |
| `group_id` | integer | required; refers to `AccountGroup.id` (one) |
| `broker_id` | integer | required; refers to `Broker.id` (one) |
| `instance_id` | integer | required; refers to `Instance.id` (one) |
| `base_currency_id` | integer | required; refers to `Currency.id` (one) |
| `username` | string | required |
| `password` | string | required; credential, stored at rest with `encrypted` treatment |
| `leverage` | integer | required |
| `balance` | decimal | default `0` |
| `account_type` | string | required |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

Unique together: (`group_id`, `broker_id`, `instance_id`).

```python
from model import Account

record = Account.deserialize(
    {
        "name": "Acc-1",
        "group_id": 1,
        "broker_id": 1,
        "instance_id": 1,
        "base_currency_id": 1,
        "username": "test",
        "password": "<hashed-or-encrypted-password-placeholder>",
        "leverage": 100,
        "account_type": "CFD",
    }
)
print(record.serialize()["name"])
# -> Acc-1
```

#### AccountGroup

An independent group for organizing the trading accounts of one user.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `user_id` | integer | required; refers to `User.id` (one) |
| `name` | string | required |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

Unique together: (`user_id`, `name`).

```python
from model import AccountGroup

record = AccountGroup.deserialize(
    {
        "user_id": 1,
        "name": "Default",
    }
)
print(record.serialize()["user_id"])
# -> 1
```

#### Action

How a position must be opened: the asset and account, and the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `name` | string | required |
| `action_group_id` | integer | required; refers to `ActionGroup.id` (one) |
| `asset_id` | integer | required; refers to `Asset.id` (one) |
| `account_id` | integer | required; refers to `Account.id` (one) |
| `partial_group_id` | integer | required; refers to `PartialGroup.id` (one) |
| `trailing_group_id` | integer | required; refers to `TrailingGroup.id` (one) |
| `risk_by_reward` | decimal | required |
| `take_profit` | decimal | required |
| `stop_loss` | decimal | required |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

Unique together: (`action_group_id`, `name`).

```python
from model import Action

record = Action.deserialize(
    {
        "name": "Default",
        "action_group_id": 1,
        "asset_id": 1,
        "account_id": 1,
        "partial_group_id": 1,
        "trailing_group_id": 1,
        "risk_by_reward": "1",
        "take_profit": "1",
        "stop_loss": "1",
    }
)
print(record.serialize()["name"])
# -> Default
```

#### ActionGroup

An independent grouping of trading actions by risk profile, such as high, normal, or low risk.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `user_id` | integer | required; refers to `User.id` (one) |
| `name` | string | required |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

Unique together: (`user_id`, `name`).

```python
from model import ActionGroup

record = ActionGroup.deserialize(
    {
        "user_id": 1,
        "name": "Default",
    }
)
print(record.serialize()["user_id"])
# -> 1
```

#### Asset

An asset that can be selected for trading, with the category that tells the system what is being traded.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `broker_id` | integer | required; refers to `Broker.id` (one) |
| `symbol` | string | required |
| `category` | string | required |
| `point_size` | float | default `0.0` |
| `digits` | integer | default `0` |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

Unique together: (`broker_id`, `symbol`).

```python
from model import Asset

record = Asset.deserialize(
    {
        "broker_id": 1,
        "symbol": "EUR/USD",
        "category": "Currency",
        "point_size": 0.0001,
        "digits": 5,
    }
)
print(record.serialize()["broker_id"])
# -> 1
```

#### Broker

A broker supported by the system, owned by one user and not coupled to any Trading Platform.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `name` | string | required |
| `user_id` | integer | required; refers to `User.id` (one) |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

Unique together: (`user_id`, `name`).

```python
from model import Broker

record = Broker.deserialize(
    {
        "name": "FxPro",
        "user_id": 1,
    }
)
print(record.serialize()["name"])
# -> FxPro
```

#### Currency

A currency the trading system can use, with its standard code, display symbol, country or region, and monetary decimal precision.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `user_id` | integer | required; refers to `User.id` (one) |
| `code` | string | required; exactly 3 characters |
| `symbol` | string | optional |
| `country` | string | optional |
| `decimal_digits` | integer | default `2` |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

Unique together: (`user_id`, `code`).

```python
from model import Currency

record = Currency.deserialize(
    {
        "user_id": 1,
        "code": "USD",
        "symbol": "$",
        "country": "United States",
        "decimal_digits": 2,
    }
)
print(record.serialize()["user_id"])
# -> 1
```

#### Instance

A user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `user_id` | integer | required; refers to `User.id` (one) |
| `trading_platform_id` | integer | required; refers to `TradingPlatform.id` (one) |
| `name` | string | required |
| `ip` | string | optional |
| `username` | string | optional |
| `password` | string | optional; credential, stored at rest with `encrypted` treatment |
| `api_key` | string | optional; credential, stored at rest with `encrypted` treatment |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

Unique together: (`user_id`, `name`).

```python
from model import Instance

record = Instance.deserialize(
    {
        "user_id": 1,
        "trading_platform_id": 1,
        "name": "MetaTrader",
        "ip": "127.0.0.1",
        "username": "test",
        "password": "<hashed-or-encrypted-password-placeholder>",
        "api_key": "<api-key-placeholder>",
    }
)
print(record.serialize()["user_id"])
# -> 1
```

#### PartialGroup

An independent group of rules that manage closing portions of an open trade.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `user_id` | integer | required; refers to `User.id` (one) |
| `name` | string | required |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

Unique together: (`user_id`, `name`).

```python
from model import PartialGroup

record = PartialGroup.deserialize(
    {
        "user_id": 1,
        "name": "Default",
    }
)
print(record.serialize()["user_id"])
# -> 1
```

#### PartialRule

An individual Partial Close rule: the profit condition under which part of an open position is closed and how much of its volume.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `name` | string | required; unique |
| `partial_group_id` | integer | required; refers to `PartialGroup.id` (one) |
| `profit_percentage` | decimal | required |
| `close_percentage` | decimal | required |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

Unique together: (`partial_group_id`, `profit_percentage`).

```python
from model import PartialRule

record = PartialRule.deserialize(
    {
        "name": "Half-at-50",
        "partial_group_id": 1,
        "profit_percentage": "50",
        "close_percentage": "50",
    }
)
print(record.serialize()["name"])
# -> Half-at-50
```

#### Position

The complete information of every position the system creates, whether opened or still pending execution.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `user_id` | integer | required; refers to `User.id` (one) |
| `name` | string | required; unique |
| `trading_platform_id` | integer | required; refers to `TradingPlatform.id` (one) |
| `broker_id` | integer | required; refers to `Broker.id` (one) |
| `account_id` | integer | required; refers to `Account.id` (one) |
| `trailing_group_id` | integer | required; refers to `TrailingGroup.id` (one) |
| `partial_group_id` | integer | required; refers to `PartialGroup.id` (one) |
| `action_group_id` | integer | required; refers to `ActionGroup.id` (one) |
| `action_id` | integer | required; refers to `Action.id` (one) |
| `date` | datetime | required |
| `volume` | decimal | required |
| `profit` | decimal | default `0` |
| `is_executed` | boolean | default `False` |
| `order_type` | string | required |
| `base_tp` | decimal | required |
| `base_sl` | decimal | required |
| `real_tp` | decimal | required |
| `real_sl` | decimal | required |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

```python
from model import Position

record = Position.deserialize(
    {
        "user_id": 1,
        "name": "Pos-1",
        "trading_platform_id": 1,
        "broker_id": 1,
        "account_id": 1,
        "trailing_group_id": 1,
        "partial_group_id": 1,
        "action_group_id": 1,
        "action_id": 1,
        "date": "2026-03-01T10:00:00+00:00",
        "volume": "0.10",
        "order_type": "market",
        "base_tp": "1.1100",
        "base_sl": "1.0900",
        "real_tp": "1.1100",
        "real_sl": "1.0900",
    }
)
print(record.serialize()["user_id"])
# -> 1
```

#### TradingPlatform

A supported trading API standard, kept independent of any specific exchange or broker.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `name` | string | required; unique |
| `code` | string | required |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

```python
from model import TradingPlatform

record = TradingPlatform.deserialize(
    {
        "name": "MetaTrader 5",
        "code": "metatrader_5",
    }
)
print(record.serialize()["name"])
# -> MetaTrader 5
```

#### TrailingGroup

An independent group of rules that manage Stop Loss and Take Profit during a trade.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `user_id` | integer | required; refers to `User.id` (one) |
| `name` | string | required |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

Unique together: (`user_id`, `name`).

```python
from model import TrailingGroup

record = TrailingGroup.deserialize(
    {
        "user_id": 1,
        "name": "Default",
    }
)
print(record.serialize()["user_id"])
# -> 1
```

#### TrailingRule

An individual rule within a Trailing Group that says when and how Take Profit and Stop Loss are adjusted.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `name` | string | required; unique |
| `trailing_group_id` | integer | required; refers to `TrailingGroup.id` (one) |
| `trigger_percentage` | decimal | required |
| `take_profit_adjustment` | decimal | optional |
| `stop_loss_adjustment` | decimal | optional |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

Unique together: (`trailing_group_id`, `trigger_percentage`).

```python
from model import TrailingRule

record = TrailingRule.deserialize(
    {
        "name": "Trail-at-50",
        "trailing_group_id": 1,
        "trigger_percentage": "50",
        "take_profit_adjustment": "10",
        "stop_loss_adjustment": "5",
    }
)
print(record.serialize()["name"])
# -> Trail-at-50
```

#### User

An independent user of the system. Each user has a separate set of settings, so new users can be added without affecting existing ones.

| Field | Type | Rules |
|---|---|---|
| `id` | integer | generated identity |
| `name` | string | required; unique |
| `username` | string | required; unique |
| `password` | string | required; credential, stored at rest with `hash` treatment |
| `api_key` | string | required; credential, stored at rest with `hash` treatment |
| `is_active` | boolean | default `True`; activation |
| `description` | string | optional |

```python
from model import User

record = User.deserialize(
    {
        "name": "Admin",
        "username": "admin",
        "password": "<hashed-or-encrypted-password-placeholder>",
        "api_key": "<api-key-placeholder>",
    }
)
print(record.serialize()["name"])
# -> Admin
```

## Setup

Requires Python 3.14 or newer and [uv](https://docs.astral.sh/uv/). From this Component's root:

```bash
uv sync
```

This creates an isolated environment and installs Model's dependency, Pydantic 2.x, together with the quality
tools (ruff and pyright). To use Model from another project, add it as a path dependency:

```bash
uv add --editable ../model
```

Model needs no configuration and reads no environment variables or secrets. It has no runtime settings.

## Run

Model is a library and runs nothing by itself. Import it and use the Operations shown above:

```python
from model import User

print(User.declaration().name)
# -> User
```

## Verify

Model has no test suite: it is outside the project's declared testing scope. Verify the Component with its
quality tools and a smoke check:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run python -c "import model; print(len(model.__all__))"
# -> 15
```

## Troubleshooting

* **`ValidationError` on `deserialize`.** Read `error.errors()`: each entry's `loc` names the offending Field and
  `msg` says why. Typical causes are a missing required Field, an unknown key, a null in a Field that is not
  optional, or a value of the wrong kind.
* **A date and time is rejected.** `Position.date` must state its timezone. Give `"2026-03-01T10:00:00+00:00"`
  or a timezone-aware `datetime`; a date and time without a timezone is ambiguous and is refused. Every accepted
  value is held in UTC and names the same instant.
* **A number is rejected as the wrong kind.** Integers, booleans, and floats are not converted from text.
  Exact decimals are the exception: give them as text such as `"0.10"` or as `Decimal`, never as a float.
* **`ImportError` for a name.** Only the fifteen definitions listed under Interface are published; import them
  from `model` directly.

## Rules a definition does not evaluate

Model checks only rules that can be decided from a single record's own data. The following Target rules cannot
be, so a definition preserves them as meaning but does not evaluate them; the Component that holds the records
must enforce them:

* **Instance connection Fields.** The Trading Platform selected for an Instance decides which of its optional
  connection Fields (`ip`, `username`, `password`, `api_key`) are required; each must be present before the
  Instance can be used. An Instance record alone cannot tell.
* **Account and Instance credentials.** The same credential must not be duplicated across an Instance and an
  Account unless the selected Trading Platform explicitly requires it in both roles.
* **Uniqueness across records.** Single-Field `unique` and the *unique together* sets are declared here; the
  Component that stores the records enforces them.
* **Existence of related records.** A relationship declares which definition it refers to; whether the referred
  record exists is decided where the records are held.
* **Credential treatment.** Credential Fields are classified with the at-rest treatment the Target requires
  (`hash` or `encrypted`); Model never applies it. Values in the examples above are placeholders.

# Model

Reusable library that defines and publishes the data-model Entities of the Trading Assistant. Every Entity is flat, carries its own meaning, and refers to other Entities only through explicit References.

```python
from model.interface import User

user = User(name="Admin", username="admin", password="example-only", api_key="example-only")
print(user.is_active)  # True
print(User.declaration.field("password").sensitivity)  # password
```

## Interface

Every Entity below is published by `model.interface`. Each Entity also has a `declaration` attribute that records the same meaning as structured data. Each Entity has an integer `id` Primary Key that increments automatically.

### User

Independent user of the system.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `name` | string | No | — | Unique |
| `username` | string | No | — | Unique |
| `password` | string | No | — | Sensitivity: password |
| `api_key` | string | No | — | Sensitivity: sensitive |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

### Trading Platform

Supported trading API standard, independent of any specific exchange or broker.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `name` | string | No | — | Unique |
| `code` | string | No | — | — |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

### Instance

User-owned connection through which the system accesses a Trading Platform.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `user_id` | integer | No | — | Reference to `User.id` |
| `trading_platform_id` | integer | No | — | Reference to `TradingPlatform.id` |
| `name` | string | No | — | — |
| `ip` | string | Yes | — | — |
| `username` | string | Yes | — | — |
| `password` | string | Yes | — | Sensitivity: password |
| `api_key` | string | Yes | — | Sensitivity: sensitive |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

Unique together: `user_id` + `name`.

### Currency

Currency usable by the trading system, with its standard code, symbol, region, and decimal precision.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `user_id` | integer | No | — | Reference to `User.id` |
| `code` | string | No | — | Maximum length 3 |
| `symbol` | string | Yes | — | — |
| `country` | string | Yes | — | — |
| `decimal_digits` | integer | No | `2` | — |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

Unique together: `user_id` + `code`.

### Broker

Supported broker owned by a user, independent of any one Trading Platform.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `name` | string | No | — | — |
| `user_id` | integer | No | — | Reference to `User.id` |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

Unique together: `user_id` + `name`.

### Asset

Tradable asset provided by a broker, with its category.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `broker_id` | integer | No | — | Reference to `Broker.id` |
| `symbol` | string | No | — | — |
| `category` | string | No | — | — |
| `point_size` | float | No | `0.0` | — |
| `digits` | integer | No | `0` | — |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

Unique together: `broker_id` + `symbol`.

### Account Group

Independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `user_id` | integer | No | — | Reference to `User.id` |
| `name` | string | No | — | — |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

Unique together: `user_id` + `name`.

### Account

Funded trading account through which the system executes trades and launches positions.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `name` | string | No | — | Unique |
| `group_id` | integer | No | — | Reference to `AccountGroup.id` |
| `broker_id` | integer | No | — | Reference to `Broker.id` |
| `instance_id` | integer | No | — | Reference to `Instance.id` |
| `base_currency_id` | integer | No | — | Reference to `Currency.id` |
| `username` | string | No | — | — |
| `password` | string | No | — | Sensitivity: password |
| `leverage` | integer | No | — | — |
| `balance` | decimal | No | `0` | — |
| `account_type` | string | No | — | — |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

Unique together: `group_id` + `broker_id` + `instance_id`.

### Trailing Group

Independent group organizing the rules that manage Stop Loss and Take Profit during a trade.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `user_id` | integer | No | — | Reference to `User.id` |
| `name` | string | No | — | — |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

Unique together: `user_id` + `name`.

### Trailing Rule

Individual rule within a Trailing Group stating when and how Take Profit and Stop Loss change.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `name` | string | No | — | Unique |
| `trailing_group_id` | integer | No | — | Reference to `TrailingGroup.id` |
| `trigger_percentage` | decimal | No | — | — |
| `take_profit_adjustment` | decimal | Yes | — | — |
| `stop_loss_adjustment` | decimal | Yes | — | — |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

Unique together: `trailing_group_id` + `trigger_percentage`.

### Partial Group

Independent group of rules for closing portions of an open trade.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `user_id` | integer | No | — | Reference to `User.id` |
| `name` | string | No | — | — |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

Unique together: `user_id` + `name`.

### Partial Rule

Individual Partial Close rule stating when part of an open position closes and how much.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `name` | string | No | — | Unique |
| `partial_group_id` | integer | No | — | Reference to `PartialGroup.id` |
| `profit_percentage` | decimal | No | — | — |
| `close_percentage` | decimal | No | — | — |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

Unique together: `partial_group_id` + `profit_percentage`.

### Action Group

Independent grouping of trading actions by risk profile.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `user_id` | integer | No | — | Reference to `User.id` |
| `name` | string | No | — | — |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

Unique together: `user_id` + `name`.

### Action

Description of how a position must be opened, with its asset, account, risk, and management groups.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `name` | string | No | — | — |
| `action_group_id` | integer | No | — | Reference to `ActionGroup.id` |
| `asset_id` | integer | No | — | Reference to `Asset.id` |
| `account_id` | integer | No | — | Reference to `Account.id` |
| `partial_group_id` | integer | No | — | Reference to `PartialGroup.id` |
| `trailing_group_id` | integer | No | — | Reference to `TrailingGroup.id` |
| `risk_by_reward` | decimal | No | — | — |
| `take_profit` | decimal | No | — | — |
| `stop_loss` | decimal | No | — | — |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

Unique together: `action_group_id` + `name`.

### Position

Complete record of a position created by the system, whether opened or pending execution.

| Field | Type | Nullable | Default | Rules |
|---|---|---|---|---|
| `id` | integer | No | — | Primary Key; Auto Increment |
| `user_id` | integer | No | — | Reference to `User.id` |
| `name` | string | No | — | Unique |
| `trading_platform_id` | integer | No | — | Reference to `TradingPlatform.id` |
| `broker_id` | integer | No | — | Reference to `Broker.id` |
| `account_id` | integer | No | — | Reference to `Account.id` |
| `trailing_group_id` | integer | No | — | Reference to `TrailingGroup.id` |
| `partial_group_id` | integer | No | — | Reference to `PartialGroup.id` |
| `action_group_id` | integer | No | — | Reference to `ActionGroup.id` |
| `action_id` | integer | No | — | Reference to `Action.id` |
| `date` | datetime | No | — | — |
| `volume` | decimal | No | — | — |
| `profit` | decimal | No | `0` | — |
| `is_executed` | boolean | No | `False` | — |
| `order_type` | string | No | — | — |
| `base_tp` | decimal | No | — | — |
| `base_sl` | decimal | No | — | — |
| `real_tp` | decimal | No | — | — |
| `real_sl` | decimal | No | — | — |
| `is_active` | boolean | No | `True` | — |
| `description` | string | Yes | — | — |

## Foundation

Foundation gives every Entity one shared implementation of conversion to and from JSON. It adds no Field or constraint.

### Convert an Entity to JSON

```python
from model.interface import Currency

usd = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(usd.to_json())
```

### Construct an Entity from JSON

```python
from model.interface import Currency

usd = Currency.from_json('{"user_id": 1, "code": "USD", "symbol": "$", "country": "United States"}')
print(usd.decimal_digits)  # 2
```

### Complete example

```python
from datetime import UTC, datetime
from decimal import Decimal

from model.interface import Position

position = Position(
    user_id=1, name="P-1", trading_platform_id=1, broker_id=1, account_id=1, trailing_group_id=1,
    partial_group_id=1, action_group_id=1, action_id=1, date=datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC),
    volume=Decimal("0.10"), order_type="buy", base_tp=Decimal("1.2"), base_sl=Decimal("1.1"),
    real_tp=Decimal("1.2"), real_sl=Decimal("1.1"),
)
text = position.to_json()  # decimal and datetime values become strings
restored = Position.from_json(text)  # and are restored to Decimal and timezone-aware datetime
assert restored == position
```

## Setup

Model requires Python 3.14 or newer and is managed with `uv`.

```bash
cd model
uv sync
```

To use Model from another Component, add it as a dependency of that Component:

```bash
uv add --editable <path to the model directory>
```

## Use

Import Entities from `model.interface`. Use `Entity.declaration` to read an Entity's meaning as structured data, and `model.declaration` and `model.foundation` directly when you need their classes.

```python
from model.interface import Broker

print([f.name for f in Broker.declaration.fields])
print([(r.field, r.entity) for r in Broker.declaration.references])
```

Import every Entity you need before using `SQLModel.metadata`, because an Entity registers its table only when it is imported. Table names are SQLModel's defaults, the lowercase Entity class name (for example `tradingplatform`), and foreign keys point to those tables.

## Troubleshooting

- **`from_json` raises a validation error.** The JSON must be an object, values must match the Field Types, and every required Field must be present. Datetime values must include a timezone offset.
- **A decimal or datetime comes back as text.** Use `Entity.from_json`, not `model_validate_json`. On an Entity, `model_validate_json` skips value conversion and leaves decimals and datetimes as strings.
- **An Entity built directly accepts a wrong value.** Constructing an Entity by calling its class does not validate values. Build from data with `Entity.model_validate(data)` or `Entity.from_json(text)` to validate.
- **`ImportError` for `model.interface`.** Confirm Model is installed in the active environment and that its Python requirement (3.14 or newer) is met.

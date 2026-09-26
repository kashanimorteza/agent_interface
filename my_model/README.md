# my_model

Reusable Model library of the Trading Assistant. It defines flat, technology-independent Domain
Entities; every Entity is a public SQLModel table model that keeps its declared meaning in a
`ModelDeclaration`. Model owns Entities only: it holds no records, storage operations, or workflow.

## Overview

```python
from my_model.model_interface import Currency

usd = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(usd.code, usd.decimal_digits)
```

Output:

```text
USD 2
```

## Interface

Import any Entity from `my_model.model_interface`. The Declaration (`my_model.model_declaration`),
Foundation (`my_model.model_foundation`), and each Entity unit (`my_model.entity.<name>`) are public too.
Every Entity has an integer `id` identity, generated automatically.

### User

Defines an independent user of the system and enables multi-user operation.

Kind: Entity. Import: `from my_model.model_interface import User`.

Construction: call `User` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `User.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `name` | string | no | — | unique |
| `username` | string | no | — | unique |
| `password` | string | no | — | sensitive |
| `api_key` | string | no | — | sensitive |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

### TradingPlatform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker.

Kind: Entity. Import: `from my_model.model_interface import TradingPlatform`.

Construction: call `TradingPlatform` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `TradingPlatform.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `name` | string | no | — | unique |
| `code` | string | no | — | — |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

Kind: Entity. Import: `from my_model.model_interface import Instance`.

Construction: call `Instance` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `Instance.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `user_id` | integer | no | — | references User |
| `trading_platform_id` | integer | no | — | references Trading Platform |
| `name` | string | no | — | — |
| `ip` | string | yes | — | — |
| `username` | string | yes | — | — |
| `password` | string | yes | — | sensitive |
| `api_key` | string | yes | — | sensitive |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

Unique together: `user_id`, `name`.

### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

Kind: Entity. Import: `from my_model.model_interface import Currency`.

Construction: call `Currency` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `Currency.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `user_id` | integer | no | — | references User |
| `code` | string | no | — | max length 3 |
| `symbol` | string | yes | — | — |
| `country` | string | yes | — | — |
| `decimal_digits` | integer | no | `2` | — |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

Unique together: `user_id`, `code`.

### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

Kind: Entity. Import: `from my_model.model_interface import Broker`.

Construction: call `Broker` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `Broker.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `name` | string | no | — | — |
| `user_id` | integer | no | — | references User |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

Unique together: `user_id`, `name`.

### Asset

Defines an asset that can be selected for trading.

Kind: Entity. Import: `from my_model.model_interface import Asset`.

Construction: call `Asset` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `Asset.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `broker_id` | integer | no | — | references Broker |
| `symbol` | string | no | — | — |
| `category` | string | no | — | — |
| `point_size` | float | no | `0.0` | — |
| `digits` | integer | no | `0` | — |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

Unique together: `broker_id`, `symbol`.

### AccountGroup

Defines an independent group for organizing trading accounts owned by one user.

Kind: Entity. Import: `from my_model.model_interface import AccountGroup`.

Construction: call `AccountGroup` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `AccountGroup.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `user_id` | integer | no | — | references User |
| `name` | string | no | — | — |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

Unique together: `user_id`, `name`.

### Account

Defines a funded trading account through which the system executes trades and launches positions.

Kind: Entity. Import: `from my_model.model_interface import Account`.

Construction: call `Account` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `Account.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `name` | string | no | — | unique |
| `group_id` | integer | no | — | references Account Group |
| `broker_id` | integer | no | — | references Broker |
| `instance_id` | integer | no | — | references Instance |
| `base_currency_id` | integer | no | — | references Currency |
| `username` | string | no | — | — |
| `password` | string | no | — | sensitive |
| `leverage` | integer | no | — | — |
| `balance` | decimal | no | `Decimal('0')` | — |
| `account_type` | string | no | — | — |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

Unique together: `group_id`, `broker_id`, `instance_id`.

### TrailingGroup

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade.

Kind: Entity. Import: `from my_model.model_interface import TrailingGroup`.

Construction: call `TrailingGroup` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `TrailingGroup.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `user_id` | integer | no | — | references User |
| `name` | string | no | — | — |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

Unique together: `user_id`, `name`.

### TrailingRule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss.

Kind: Entity. Import: `from my_model.model_interface import TrailingRule`.

Construction: call `TrailingRule` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `TrailingRule.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `name` | string | no | — | unique |
| `trailing_group_id` | integer | no | — | references Trailing Group |
| `trigger_percentage` | decimal | no | — | — |
| `take_profit_adjustment` | decimal | yes | — | — |
| `stop_loss_adjustment` | decimal | yes | — | — |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

Unique together: `trailing_group_id`, `trigger_percentage`.

### PartialGroup

Defines an independent group of rules for managing portions of an open trade.

Kind: Entity. Import: `from my_model.model_interface import PartialGroup`.

Construction: call `PartialGroup` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `PartialGroup.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `user_id` | integer | no | — | references User |
| `name` | string | no | — | — |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

Unique together: `user_id`, `name`.

### PartialRule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

Kind: Entity. Import: `from my_model.model_interface import PartialRule`.

Construction: call `PartialRule` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `PartialRule.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `name` | string | no | — | unique |
| `partial_group_id` | integer | no | — | references Partial Group |
| `profit_percentage` | decimal | no | — | — |
| `close_percentage` | decimal | no | — | — |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

Unique together: `partial_group_id`, `profit_percentage`.

### ActionGroup

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk.

Kind: Entity. Import: `from my_model.model_interface import ActionGroup`.

Construction: call `ActionGroup` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `ActionGroup.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `user_id` | integer | no | — | references User |
| `name` | string | no | — | — |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

Unique together: `user_id`, `name`.

### Action

Defines how a position must be opened.

Kind: Entity. Import: `from my_model.model_interface import Action`.

Construction: call `Action` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `Action.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `name` | string | no | — | — |
| `action_group_id` | integer | no | — | references Action Group |
| `asset_id` | integer | no | — | references Asset |
| `account_id` | integer | no | — | references Account |
| `partial_group_id` | integer | no | — | references Partial Group |
| `trailing_group_id` | integer | no | — | references Trailing Group |
| `risk_by_reward` | decimal | no | — | — |
| `take_profit` | decimal | no | — | — |
| `stop_loss` | decimal | no | — | — |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

Unique together: `action_group_id`, `name`.

### Position

Stores the complete information for every position created by the system.

Kind: Entity. Import: `from my_model.model_interface import Position`.

Construction: call `Position` directly with keyword arguments named by the Fields below. JSON: `to_json()` converts an instance to a JSON string and `Position.from_json()` creates a validated instance from one.

| Field | Type | Nullable | Default | Notes |
| --- | --- | --- | --- | --- |
| `id` | integer | no | — | identity, auto increment |
| `user_id` | integer | no | — | references User |
| `name` | string | no | — | unique |
| `trading_platform_id` | integer | no | — | references Trading Platform |
| `broker_id` | integer | no | — | references Broker |
| `account_id` | integer | no | — | references Account |
| `trailing_group_id` | integer | no | — | references Trailing Group |
| `partial_group_id` | integer | no | — | references Partial Group |
| `action_group_id` | integer | no | — | references Action Group |
| `action_id` | integer | no | — | references Action |
| `date` | datetime | no | — | — |
| `volume` | decimal | no | — | — |
| `profit` | decimal | no | `Decimal('0')` | — |
| `is_executed` | boolean | no | `False` | — |
| `order_type` | string | no | — | — |
| `base_tp` | decimal | no | — | — |
| `base_sl` | decimal | no | — | — |
| `real_tp` | decimal | no | — | — |
| `real_sl` | decimal | no | — | — |
| `is_active` | boolean | no | `True` | — |
| `description` | string | yes | — | — |

## Foundation

Every Entity adopts `ModelFoundation`, which provides two capabilities and defines no Fields.

### `to_json()`

Converts an instance to a JSON string.

```python
from my_model.model_interface import Currency

print(Currency(user_id=1, code="EUR", decimal_digits=2).to_json())
```

Output:

```text
{"user_id":1,"code":"EUR","decimal_digits":2,"id":null,"symbol":null,"country":null,"is_active":true,"description":null}
```

### `from_json()`

Creates a validated instance of the calling Entity from a JSON string or bytes.

```python
from my_model.model_interface import Currency

currency = Currency.from_json('{"user_id": 1, "code": "GBP"}')
print(currency.code, currency.decimal_digits)
```

Output:

```text
GBP 2
```

### Complete example

```python
from my_model.model_interface import Broker

broker = Broker(user_id=1, name="FxPro")
restored = Broker.from_json(broker.to_json())
print(restored == broker, restored.name)
```

Output:

```text
True FxPro
```

## Setup

Requires Python 3.14 or newer and [uv](https://docs.astral.sh/uv/).

```bash
cd my_model
uv sync
```

## Run

Model is a library, so there is nothing to launch. Use it from Python:

```bash
uv run python -c "from my_model.model_interface import User; print(User.declaration.entity)"
```

Output:

```text
User
```

Quality checks:

```bash
uv run ruff format src
uv run ruff check src
uv run pyright src
```

## Troubleshooting

- **A wrong value is accepted when constructing an Entity directly.** Table models skip validation on
  direct construction. Use `Entity.from_json(...)` or `Entity.model_validate(...)` for untrusted data.
- **`ModuleNotFoundError: my_model`.** Run inside the project environment with `uv run`, or install the
  library into your environment.
- **`uv sync` cannot find a compatible Python.** The library requires Python 3.14 or newer; let uv
  download it (`uv python install 3.14`) and rerun `uv sync`.

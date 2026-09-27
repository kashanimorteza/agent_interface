# my_model

Technology-independent domain Entities for the Trading Assistant. Every Entity is a flat, stand-alone class with its
fields, keys, references, uniqueness, defaults, and sensitive flags recorded once, so Logic can use it directly and
Database can derive its tables from the same class.

## Overview

```python
from my_model.model_interface import Currency

usd = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(usd.code, usd.decimal_digits)  # USD 2
```

## Interface

Every public Entity is presented by `my_model.model_interface`. Each Entity also carries a `declaration` class attribute
that records its meaning. The tables below list each Entity's fields.

### User

An independent user of the system, enabling multi-user operation with separate settings.

- **Kind:** Entity.
- **Import:** `User` from `my_model.model_interface`.
- **Direct construction:** call `User` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `User.from_json(...)` on the class.
- **Unique:** (`name`); (`username`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `name` | string | no |  | no |  | The user's display name. |
| `username` | string | no |  | no |  | The username used to identify the user. |
| `password` | string | no |  | yes |  | The password credential used by the user. |
| `api_key` | string | no |  | yes |  | The API key assigned to the user. |
| `is_active` | boolean | no | True | no |  | Indicates whether the user is active. |
| `description` | string | yes |  | no |  | Describes the user. |

### TradingPlatform

A supported trading API standard, independent of any specific exchange or broker.

- **Kind:** Entity.
- **Import:** `TradingPlatform` from `my_model.model_interface`.
- **Direct construction:** call `TradingPlatform` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `TradingPlatform.from_json(...)` on the class.
- **Unique:** (`name`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `name` | string | no |  | no |  | The platform's display name. |
| `code` | string | no |  | no |  | Identifies the implementation class the application must use for this trading platform. |
| `is_active` | boolean | no | True | no |  | Indicates whether the platform is active. |
| `description` | string | yes |  | no |  | Describes the platform. |

### Instance

A user-owned connection instance through which the system accesses a supported Trading Platform.

- **Kind:** Entity.
- **Import:** `Instance` from `my_model.model_interface`.
- **Direct construction:** call `Instance` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `Instance.from_json(...)` on the class.
- **Unique:** (`user_id`, `name`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `user_id` | integer | no |  | no | User.id | Identifies the user who owns this instance. |
| `trading_platform_id` | integer | no |  | no | TradingPlatform.id | Identifies the trading platform used by this instance. |
| `name` | string | no |  | no |  | The instance's display name. |
| `ip` | string | yes |  | no |  | The technical network address used to reach the Trading Platform when required. |
| `username` | string | yes |  | no |  | The technical username used to establish the Instance connection when required. |
| `password` | string | yes |  | yes |  | The technical password used to establish the Instance connection when required. |
| `api_key` | string | yes |  | yes |  | The technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | no | True | no |  | Indicates whether the instance is active. |
| `description` | string | yes |  | no |  | Describes the instance. |

### Currency

A currency usable by the trading system, with its standard code, symbol, region, and decimal precision.

- **Kind:** Entity.
- **Import:** `Currency` from `my_model.model_interface`.
- **Direct construction:** call `Currency` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `Currency.from_json(...)` on the class.
- **Unique:** (`user_id`, `code`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `user_id` | integer | no |  | no | User.id | Identifies the user who owns this currency. |
| `code` | string(3) | no |  | no |  | The currency's standard three-letter code, such as USD or EUR. |
| `symbol` | string | yes |  | no |  | The currency's display symbol. |
| `country` | string | yes |  | no |  | The country or region associated with the currency. |
| `decimal_digits` | integer | no | 2 | no |  | The number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | no | True | no |  | Indicates whether the currency is active. |
| `description` | string | yes |  | no |  | Describes the currency. |

### Broker

A broker supported by the system, owned by a user and not coupled to one Trading Platform.

- **Kind:** Entity.
- **Import:** `Broker` from `my_model.model_interface`.
- **Direct construction:** call `Broker` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `Broker.from_json(...)` on the class.
- **Unique:** (`user_id`, `name`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `name` | string | no |  | no |  | The broker's display name. |
| `user_id` | integer | no |  | no | User.id | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | no | True | no |  | Indicates whether the broker is active. |
| `description` | string | yes |  | no |  | Describes the broker. |

### Asset

An asset that can be selected for trading, with its category.

- **Kind:** Entity.
- **Import:** `Asset` from `my_model.model_interface`.
- **Direct construction:** call `Asset` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `Asset.from_json(...)` on the class.
- **Unique:** (`broker_id`, `symbol`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `broker_id` | integer | no |  | no | Broker.id | Identifies the broker that provides this asset. |
| `symbol` | string | no |  | no |  | Identifies the tradable asset. |
| `category` | string | no |  | no |  | Identifies the asset category, such as Currency, Commodity, or Cryptocurrency. |
| `point_size` | float | no | 0.0 | no |  | The size of one point for the asset. |
| `digits` | integer | no | 0 | no |  | The number of decimal digits used for the asset's price. |
| `is_active` | boolean | no | True | no |  | Indicates whether the asset is active. |
| `description` | string | yes |  | no |  | Describes the asset. |

### AccountGroup

An independent group for organizing trading accounts owned by one user.

- **Kind:** Entity.
- **Import:** `AccountGroup` from `my_model.model_interface`.
- **Direct construction:** call `AccountGroup` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `AccountGroup.from_json(...)` on the class.
- **Unique:** (`user_id`, `name`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `user_id` | integer | no |  | no | User.id | Identifies the user who owns the account group. |
| `name` | string | no |  | no |  | The account group's display name. |
| `is_active` | boolean | no | True | no |  | Indicates whether the account group is active. |
| `description` | string | yes |  | no |  | Describes the account group. |

### Account

A funded trading account through which the system executes trades and launches positions.

- **Kind:** Entity.
- **Import:** `Account` from `my_model.model_interface`.
- **Direct construction:** call `Account` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `Account.from_json(...)` on the class.
- **Unique:** (`name`); (`group_id`, `broker_id`, `instance_id`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `name` | string | no |  | no |  | The account's display name. |
| `group_id` | integer | no |  | no | AccountGroup.id | Identifies the account group that contains the account. |
| `broker_id` | integer | no |  | no | Broker.id | Identifies the broker that owns the account. |
| `instance_id` | integer | no |  | no | Instance.id | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | no |  | no | Currency.id | Identifies the base currency used by the account. |
| `username` | string | no |  | no |  | The username identifier used to access the trading account. |
| `password` | string | no |  | yes |  | The credential used to access the trading account. |
| `leverage` | integer | no |  | no |  | The account's leverage multiplier. |
| `balance` | decimal | no | 0 | no |  | The account's current balance. |
| `account_type` | string | no |  | no |  | Identifies the account model, such as cfd or spread_betting. |
| `is_active` | boolean | no | True | no |  | Indicates whether the account is active. |
| `description` | string | yes |  | no |  | Describes the account. |

### TrailingGroup

An independent group of rules that manage Stop Loss and Take Profit during a trade.

- **Kind:** Entity.
- **Import:** `TrailingGroup` from `my_model.model_interface`.
- **Direct construction:** call `TrailingGroup` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `TrailingGroup.from_json(...)` on the class.
- **Unique:** (`user_id`, `name`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `user_id` | integer | no |  | no | User.id | Identifies the user who owns the trailing group. |
| `name` | string | no |  | no |  | The trailing group's display name. |
| `is_active` | boolean | no | True | no |  | Indicates whether the trailing group is active. |
| `description` | string | yes |  | no |  | Describes the trailing group. |

### TrailingRule

An individual rule within a Trailing Group defining when and how to manage Take Profit and Stop Loss.

- **Kind:** Entity.
- **Import:** `TrailingRule` from `my_model.model_interface`.
- **Direct construction:** call `TrailingRule` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `TrailingRule.from_json(...)` on the class.
- **Unique:** (`name`); (`trailing_group_id`, `trigger_percentage`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `name` | string | no |  | no |  | The trailing rule's display name. |
| `trailing_group_id` | integer | no |  | no | TrailingGroup.id | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | decimal | no |  | no |  | The profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | decimal | yes |  | no |  | The take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | decimal | yes |  | no |  | The stop-loss adjustment applied when the rule is activated. |
| `is_active` | boolean | no | True | no |  | Indicates whether the trailing rule is active. |
| `description` | string | yes |  | no |  | Describes the trailing rule. |

### PartialGroup

An independent group of rules for managing portions of an open trade.

- **Kind:** Entity.
- **Import:** `PartialGroup` from `my_model.model_interface`.
- **Direct construction:** call `PartialGroup` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `PartialGroup.from_json(...)` on the class.
- **Unique:** (`user_id`, `name`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `user_id` | integer | no |  | no | User.id | Identifies the user who owns the partial group. |
| `name` | string | no |  | no |  | The partial group's display name. |
| `is_active` | boolean | no | True | no |  | Indicates whether the partial group is active. |
| `description` | string | yes |  | no |  | Describes the partial group. |

### PartialRule

An individual Partial Close rule defining when and how much of an open position is closed.

- **Kind:** Entity.
- **Import:** `PartialRule` from `my_model.model_interface`.
- **Direct construction:** call `PartialRule` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `PartialRule.from_json(...)` on the class.
- **Unique:** (`name`); (`partial_group_id`, `profit_percentage`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `name` | string | no |  | no |  | The partial rule's display name. |
| `partial_group_id` | integer | no |  | no | PartialGroup.id | Identifies the partial group that contains the rule. |
| `profit_percentage` | decimal | no |  | no |  | The profit percentage that activates the rule. |
| `close_percentage` | decimal | no |  | no |  | The percentage of the position closed when the rule is activated. |
| `is_active` | boolean | no | True | no |  | Indicates whether the partial rule is active. |
| `description` | string | yes |  | no |  | Describes the partial rule. |

### ActionGroup

An independent grouping for trading actions based on their risk profile.

- **Kind:** Entity.
- **Import:** `ActionGroup` from `my_model.model_interface`.
- **Direct construction:** call `ActionGroup` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `ActionGroup.from_json(...)` on the class.
- **Unique:** (`user_id`, `name`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `user_id` | integer | no |  | no | User.id | Identifies the user who owns the action group. |
| `name` | string | no |  | no |  | The action group's display name. |
| `is_active` | boolean | no | True | no |  | Indicates whether the action group is active. |
| `description` | string | yes |  | no |  | Describes the action group. |

### Action

Defines how a position must be opened, selecting the asset and account and the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings.

- **Kind:** Entity.
- **Import:** `Action` from `my_model.model_interface`.
- **Direct construction:** call `Action` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `Action.from_json(...)` on the class.
- **Unique:** (`action_group_id`, `name`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `name` | string | no |  | no |  | The action's display name. |
| `action_group_id` | integer | no |  | no | ActionGroup.id | Identifies the action group that contains the action. |
| `asset_id` | integer | no |  | no | Asset.id | Identifies the asset traded by the action. |
| `account_id` | integer | no |  | no | Account.id | Identifies the account used to execute the action. |
| `partial_group_id` | integer | no |  | no | PartialGroup.id | Identifies the Partial Group used by the action. |
| `trailing_group_id` | integer | no |  | no | TrailingGroup.id | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | decimal | no |  | no |  | The numeric risk-to-reward value used by the action. |
| `take_profit` | decimal | no |  | no |  | The Take Profit value used by the action. |
| `stop_loss` | decimal | no |  | no |  | The Stop Loss value used by the action. |
| `is_active` | boolean | no | True | no |  | Indicates whether the action is active. |
| `description` | string | yes |  | no |  | Describes the action. |

### Position

The complete information for every position created by the system, whether opened or pending execution.

- **Kind:** Entity.
- **Import:** `Position` from `my_model.model_interface`.
- **Direct construction:** call `Position` with keyword arguments named after its fields; `id` is assigned by storage and may be omitted.
- **JSON conversion:** `to_json()` on an instance and `Position.from_json(...)` on the class.
- **Unique:** (`name`).

| Field | Type | Nullable | Default | Sensitive | Reference | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | no |  |  |
| `user_id` | integer | no |  | no | User.id | Identifies the user who owns the position. |
| `name` | string | no |  | no |  | The position's display name. |
| `trading_platform_id` | integer | no |  | no | TradingPlatform.id | Identifies the trading platform used to execute the position. |
| `broker_id` | integer | no |  | no | Broker.id | Identifies the broker through which the position is executed. |
| `account_id` | integer | no |  | no | Account.id | Identifies the trading account used for the position. |
| `trailing_group_id` | integer | no |  | no | TrailingGroup.id | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | integer | no |  | no | PartialGroup.id | Identifies the Partial Group applied to the position. |
| `action_group_id` | integer | no |  | no | ActionGroup.id | Identifies the Action Group associated with the position. |
| `action_id` | integer | no |  | no | Action.id | Identifies the action from which the position is created. |
| `date` | datetime | no |  | no |  | The position's date and time. |
| `volume` | decimal | no |  | no |  | The position's trading volume. |
| `profit` | decimal | no | 0 | no |  | The position's current profit or loss. |
| `is_executed` | boolean | no | False | no |  | Indicates whether the position has been executed. |
| `order_type` | string | no |  | no |  | The position's order type. |
| `base_tp` | decimal | no |  | no |  | The position's initial Take Profit value. |
| `base_sl` | decimal | no |  | no |  | The position's initial Stop Loss value. |
| `real_tp` | decimal | no |  | no |  | The position's current Take Profit value. |
| `real_sl` | decimal | no |  | no |  | The position's current Stop Loss value. |
| `is_active` | boolean | no | True | no |  | Indicates whether the position is active. |
| `description` | string | yes |  | no |  | Describes the position. |

## Foundation

Every Entity gets two conversions from the shared Foundation.

`to_json()` returns an instance as a JSON string:

```python
from my_model.model_interface import Broker

broker = Broker(user_id=1, name="FxPro")
print(broker.to_json())
```

`from_json()` creates an instance from a JSON string:

```python
from my_model.model_interface import Broker

broker = Broker.from_json('{"user_id": 1, "name": "FxPro"}')
print(broker.name)  # FxPro
```

A complete example that uses both capabilities with one Entity:

```python
from my_model.model_interface import Asset

asset = Asset(broker_id=1, symbol="EUR/USD", category="Currency", point_size=0.0001, digits=5)
text = asset.to_json()
same = Asset.from_json(text)
assert same == asset
print(same.symbol, same.digits)  # EUR/USD 5
```

## Setup

The package needs Python 3.14 or later and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Run

The Model is a library, so nothing runs by itself. Import it from Python:

```bash
uv run python -c "from my_model.model_interface import User; print(User.declaration.entity)"
```

Check the source with the project's quality tools:

```bash
uv run ruff check src
uv run pyright src
```

## Troubleshooting

- **`ModuleNotFoundError: my_model`** — run `uv sync` first and run Python through `uv run`.
- **`requires-python` error during setup** — install Python 3.14 or later (`uv python install 3.14`).
- **`from_json()` raises a validation error** — the JSON keys or values do not match the Entity's fields; compare them
  with that Entity's table above.
- **A field is missing after `from_json()`** — a field left out of the JSON takes its default, or `None` when nullable.

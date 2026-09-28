# Model

## Overview

Model is the reusable data-model library of the Trading Assistant. It defines and publishes the application's Entities as flat, technology-independent definitions, each with its own Fields and explicit Relations, and provides the shared behaviour that validates an Entity and converts it to and from JSON.

```python
from model.interface import Broker

broker = Broker(name="FxPro", user_id=1)
print(broker.name, broker.is_active)
```

```text
FxPro True
```

## Interface

`model.interface` is the single entry point that publishes the Entities. It publishes exactly the Entities below, in this order, and nothing else.

In every Field table, **Required** means the Field is not nullable and has neither a Default Value nor Value Generation, so a value must be supplied when the Entity is created. **Nullable** means the Field may hold `null`. A Relation records only the local Field and the name of the target Entity and Field. No Field declares a sensitivity marker.

### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `name` | `string` | yes | no | — | — | no | — | — | The user's display name. |
| `username` | `string` | yes | no | — | — | no | — | — | The username used to identify the user. |
| `password` | `string` | yes | no | — | — | no | — | — | The password credential used by the user. |
| `api_key` | `string` | yes | no | — | — | no | — | — | The API key assigned to the user. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the user is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the user. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - None
- Uniqueness Constraints:
  - `name`
  - `username`
- Indexes:
  - None

### Trading Platform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `name` | `string` | yes | no | — | — | no | — | — | The platform's display name. |
| `code` | `string` | yes | no | — | — | no | — | — | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the platform is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the platform. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - None
- Uniqueness Constraints:
  - `name`
- Indexes:
  - None

### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `user_id` | `integer` | yes | no | — | — | no | — | — | Identifies the user who owns this instance. |
| `trading_platform_id` | `integer` | yes | no | — | — | no | — | — | Identifies the trading platform used by this instance. |
| `name` | `string` | yes | no | — | — | no | — | — | The instance's display name. |
| `ip` | `string` | no | yes | — | — | no | — | — | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | `string` | no | yes | — | — | no | — | — | Defines the technical username used to establish the Instance connection when required. |
| `password` | `string` | no | yes | — | — | no | — | — | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | `string` | no | yes | — | — | no | — | — | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the instance is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the instance. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User`.`id`
  - `trading_platform_id` → `Trading Platform`.`id`
- Uniqueness Constraints:
  - `user_id`, `name`
- Indexes:
  - None

### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `user_id` | `integer` | yes | no | — | — | no | — | — | Identifies the user who owns this currency. |
| `code` | `string` | yes | no | — | — | no | maximum length 3 | — | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | `string` | no | yes | — | — | no | — | — | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | `string` | no | yes | — | — | no | — | — | Identifies the country or region associated with the currency. |
| `decimal_digits` | `integer` | no | no | `2` | — | no | — | — | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the currency is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the currency. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User`.`id`
- Uniqueness Constraints:
  - `user_id`, `code`
- Indexes:
  - None

### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `name` | `string` | yes | no | — | — | no | — | — | The broker's display name. |
| `user_id` | `integer` | yes | no | — | — | no | — | — | Identifies the user who owns the broker configuration. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the broker is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the broker. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User`.`id`
- Uniqueness Constraints:
  - `user_id`, `name`
- Indexes:
  - None

### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `broker_id` | `integer` | yes | no | — | — | no | — | — | Identifies the broker that provides this asset. |
| `symbol` | `string` | yes | no | — | — | no | — | — | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | `string` | yes | no | — | — | no | — | — | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | `float` | no | no | `0.0` | — | no | — | — | Stores the size of one point for the asset. |
| `digits` | `integer` | no | no | `0` | — | no | — | — | Stores the number of decimal digits used for the asset's price. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the asset is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the asset. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `broker_id` → `Broker`.`id`
- Uniqueness Constraints:
  - `broker_id`, `symbol`
- Indexes:
  - None

### Account Group

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `user_id` | `integer` | yes | no | — | — | no | — | — | Identifies the user who owns the account group. |
| `name` | `string` | yes | no | — | — | no | — | — | The account group's display name. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the account group is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the account group. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User`.`id`
- Uniqueness Constraints:
  - `user_id`, `name`
- Indexes:
  - None

### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `name` | `string` | yes | no | — | — | no | — | — | The account's display name. |
| `group_id` | `integer` | yes | no | — | — | no | — | — | Identifies the account group that contains the account. |
| `broker_id` | `integer` | yes | no | — | — | no | — | — | Identifies the broker that owns the account. |
| `instance_id` | `integer` | yes | no | — | — | no | — | — | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | `integer` | yes | no | — | — | no | — | — | Identifies the base currency used by the account. |
| `username` | `string` | yes | no | — | — | no | — | — | The username identifier used to access the trading account. |
| `password` | `string` | yes | no | — | — | no | — | — | The credential used to access the trading account. |
| `leverage` | `integer` | yes | no | — | — | no | — | — | Defines the account's leverage multiplier. |
| `balance` | `decimal` | no | no | `0` | — | no | — | — | Stores the account's current balance. |
| `account_type` | `string` | yes | no | — | — | no | — | — | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the account is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the account. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `group_id` → `Account Group`.`id`
  - `broker_id` → `Broker`.`id`
  - `instance_id` → `Instance`.`id`
  - `base_currency_id` → `Currency`.`id`
- Uniqueness Constraints:
  - `name`
  - `group_id`, `broker_id`, `instance_id`
- Indexes:
  - None

### Trailing Group

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `user_id` | `integer` | yes | no | — | — | no | — | — | Identifies the user who owns the trailing group. |
| `name` | `string` | yes | no | — | — | no | — | — | The trailing group's display name. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the trailing group is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the trailing group. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User`.`id`
- Uniqueness Constraints:
  - `user_id`, `name`
- Indexes:
  - None

### Trailing Rule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `name` | `string` | yes | no | — | — | no | — | — | The trailing rule's display name. |
| `trailing_group_id` | `integer` | yes | no | — | — | no | — | — | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | `decimal` | yes | no | — | — | no | — | — | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | `decimal` | no | yes | — | — | no | — | — | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | `decimal` | no | yes | — | — | no | — | — | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the trailing rule is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the trailing rule. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `trailing_group_id` → `Trailing Group`.`id`
- Uniqueness Constraints:
  - `name`
  - `trailing_group_id`, `trigger_percentage`
- Indexes:
  - None

### Partial Group

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `user_id` | `integer` | yes | no | — | — | no | — | — | Identifies the user who owns the partial group. |
| `name` | `string` | yes | no | — | — | no | — | — | The partial group's display name. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the partial group is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the partial group. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User`.`id`
- Uniqueness Constraints:
  - `user_id`, `name`
- Indexes:
  - None

### Partial Rule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `name` | `string` | yes | no | — | — | no | — | — | The partial rule's display name. |
| `partial_group_id` | `integer` | yes | no | — | — | no | — | — | Identifies the partial group that contains the rule. |
| `profit_percentage` | `decimal` | yes | no | — | — | no | — | — | Defines the profit percentage that activates the rule. |
| `close_percentage` | `decimal` | yes | no | — | — | no | — | — | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the partial rule is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the partial rule. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `partial_group_id` → `Partial Group`.`id`
- Uniqueness Constraints:
  - `name`
  - `partial_group_id`, `profit_percentage`
- Indexes:
  - None

### Action Group

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `user_id` | `integer` | yes | no | — | — | no | — | — | Identifies the user who owns the action group. |
| `name` | `string` | yes | no | — | — | no | — | — | The action group's display name. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the action group is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the action group. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User`.`id`
- Uniqueness Constraints:
  - `user_id`, `name`
- Indexes:
  - None

### Action

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `name` | `string` | yes | no | — | — | no | — | — | The action's display name. |
| `action_group_id` | `integer` | yes | no | — | — | no | — | — | Identifies the action group that contains the action. |
| `asset_id` | `integer` | yes | no | — | — | no | — | — | Identifies the asset traded by the action. |
| `account_id` | `integer` | yes | no | — | — | no | — | — | Identifies the account used to execute the action. |
| `partial_group_id` | `integer` | yes | no | — | — | no | — | — | Identifies the Partial Group used by the action. |
| `trailing_group_id` | `integer` | yes | no | — | — | no | — | — | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | `decimal` | yes | no | — | — | no | — | — | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | `decimal` | yes | no | — | — | no | — | — | Defines the Take Profit value used by the action. |
| `stop_loss` | `decimal` | yes | no | — | — | no | — | — | Defines the Stop Loss value used by the action. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the action is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the action. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `action_group_id` → `Action Group`.`id`
  - `asset_id` → `Asset`.`id`
  - `account_id` → `Account`.`id`
  - `partial_group_id` → `Partial Group`.`id`
  - `trailing_group_id` → `Trailing Group`.`id`
- Uniqueness Constraints:
  - `action_group_id`, `name`
- Indexes:
  - None

### Position

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Required | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | `integer` | no | no | — | — | yes | — | `auto_increment` | — |
| `user_id` | `integer` | yes | no | — | — | no | — | — | Identifies the user who owns the position. |
| `name` | `string` | yes | no | — | — | no | — | — | The position's display name. |
| `trading_platform_id` | `integer` | yes | no | — | — | no | — | — | Identifies the trading platform used to execute the position. |
| `broker_id` | `integer` | yes | no | — | — | no | — | — | Identifies the broker through which the position is executed. |
| `account_id` | `integer` | yes | no | — | — | no | — | — | Identifies the trading account used for the position. |
| `trailing_group_id` | `integer` | yes | no | — | — | no | — | — | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | `integer` | yes | no | — | — | no | — | — | Identifies the Partial Group applied to the position. |
| `action_group_id` | `integer` | yes | no | — | — | no | — | — | Identifies the Action Group associated with the position. |
| `action_id` | `integer` | yes | no | — | — | no | — | — | Identifies the action from which the position is created. |
| `date` | `datetime` | yes | no | — | — | no | — | — | Stores the position's date and time. |
| `volume` | `decimal` | yes | no | — | — | no | — | — | Stores the position's trading volume. |
| `profit` | `decimal` | no | no | `0` | — | no | — | — | Stores the position's current profit or loss. |
| `is_executed` | `boolean` | no | no | `false` | — | no | — | — | Indicates whether the position has been executed. |
| `order_type` | `string` | yes | no | — | — | no | — | — | Stores the position's order type. |
| `base_tp` | `decimal` | yes | no | — | — | no | — | — | Stores the position's initial Take Profit value. |
| `base_sl` | `decimal` | yes | no | — | — | no | — | — | Stores the position's initial Stop Loss value. |
| `real_tp` | `decimal` | yes | no | — | — | no | — | — | Stores the position's current Take Profit value. |
| `real_sl` | `decimal` | yes | no | — | — | no | — | — | Stores the position's current Stop Loss value. |
| `is_active` | `boolean` | no | no | `true` | — | no | — | — | Indicates whether the position is active. |
| `description` | `string` | no | yes | — | — | no | — | — | Describes the position. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User`.`id`
  - `trading_platform_id` → `Trading Platform`.`id`
  - `broker_id` → `Broker`.`id`
  - `account_id` → `Account`.`id`
  - `trailing_group_id` → `Trailing Group`.`id`
  - `partial_group_id` → `Partial Group`.`id`
  - `action_group_id` → `Action Group`.`id`
  - `action_id` → `Action`.`id`
- Uniqueness Constraints:
  - `name`
- Indexes:
  - None

## Declaration

Every Entity carries a `Declaration` that records its meaning and Entity Metadata in one canonical contract, readable from the Entity class as `declaration`. The `Declaration` type is published by `model.core.declaration`. An Entity Declaration has the members `name`, `description`, `fields`, `primary_key`, `relations`, `unique_constraints`, and `indexes`. Each Field Declaration has `name`, `description`, `type`, `nullable`, `has_default`, `default`, `sensitivity`, `immutable`, the value constraints `length`, `minimum`, `maximum`, `pattern`, `precision`, `scale`, and `allowed_values`, and `value_generation`. Declarations are read-only.

```python
from model.interface import Currency

declaration = Currency.declaration
print(declaration.primary_key)
print([(r.local_field, r.target_entity, r.target_field) for r in declaration.relations])
print(declaration.unique_constraints)
```

```text
id
[('user_id', 'User', 'id')]
(('user_id', 'code'),)
```

## Foundation

Foundation, published by `model.core.foundation`, gives every Entity two capabilities: `to_json` converts an Entity to a JSON object, and `from_json` constructs an Entity from one. The object has exactly the Entity's Field names as keys, in Declaration order. Decimal values are exact base-10 strings, datetime values are ISO 8601 text that keeps precision and timezone offset, and an identity that has not been generated yet is `null`. When reading JSON, a decimal must be written as digits with an optional sign, fraction and exponent, and a datetime as an ISO 8601 date-time such as `2026-01-02T03:04:05+00:00` (date and time, with an optional `Z` or offset). A JSON integer is read as a float for a float Field when it is exactly representable. Anything else is rejected.

Convert an Entity to JSON:

```python
from model.interface import Asset

asset = Asset(broker_id=1, symbol="EUR/USD", category="Currency", point_size=0.0001, digits=5)
print(asset.to_json())
```

```text
{'id': None, 'broker_id': 1, 'symbol': 'EUR/USD', 'category': 'Currency', 'point_size': 0.0001, 'digits': 5, 'is_active': True, 'description': None}
```

Construct an Entity from JSON:

```python
from model.interface import Asset

asset = Asset.from_json(
    {"broker_id": 1, "symbol": "EUR/USD", "category": "Currency", "point_size": 0.0001, "digits": 5}
)
print(asset.symbol, asset.digits)
```

```text
EUR/USD 5
```

Use both capabilities together with one Entity:

```python
from datetime import datetime, timezone
from decimal import Decimal

from model.interface import Position

position = Position(
    user_id=1,
    name="EUR/USD long",
    trading_platform_id=1,
    broker_id=1,
    account_id=1,
    trailing_group_id=1,
    partial_group_id=1,
    action_group_id=1,
    action_id=1,
    date=datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
    volume=Decimal("0.10"),
    order_type="market",
    base_tp=Decimal("1.1050"),
    base_sl=Decimal("1.0950"),
    real_tp=Decimal("1.1050"),
    real_sl=Decimal("1.0950"),
)
document = position.to_json()
print(document["date"], document["volume"])
restored = Position.from_json(document)
print(restored.date == position.date, restored.volume == position.volume)
```

```text
2026-01-02T03:04:05+00:00 0.10
True True
```

## Setup

Model requires Python 3.14 or later and [uv](https://docs.astral.sh/uv/).

1. Install the package and its dependencies in an isolated environment from the Model root:

```bash
uv sync
```

2. Confirm that the Interface imports:

```bash
uv run python -c "from model.interface import User; print(User.declaration.name)"
```

```text
User
```

3. To use Model from another project, add it as a dependency from that project's root, replacing the placeholder with the path to the Model root:

```bash
uv add --editable <path-to-model>
```

## Use

Obtain Entities from `model.interface`. Create an Entity with keyword arguments; every value is validated against the Field's Type and rules, and no value is converted to another Type. Assignment is validated the same way and leaves the previous value in place when it is rejected. A rejection raises a `ValueError` whose message names the Entity and the Field and does not repeat the rejected value. A Field cannot be deleted.

```python
from model.interface import Broker

broker = Broker(name="FxPro", user_id=1)
broker.name = "FxPro EU"
print(broker.name)
try:
    broker.name = None
except ValueError as error:
    print("rejected:", str(error).splitlines()[:2])
print(broker.name)
```

```text
FxPro EU
rejected: ['1 validation error for Broker', 'name']
FxPro EU
```

Read an Entity's meaning and structure through its `declaration`, and exchange it as JSON through `to_json` and `from_json`, as shown above.

## Troubleshooting

### A value is rejected because of its Type

When you create an Entity or assign a Field, values are never converted between Types, so a string is not accepted for an integer, an integer is not accepted for a boolean or a float, and a float is not accepted for a decimal. Supply a value of the Field's Type. Reading JSON has one exception, described in the Foundation section.

```python
from model.interface import Broker

try:
    Broker(name="FxPro", user_id="1")
except ValueError as error:
    print(str(error).splitlines()[:2])
print(Broker(name="FxPro", user_id=1).user_id)
```

```text
['1 validation error for Broker', 'user_id']
1
```

### A Required Field is missing

Every Field that is not nullable and has neither a Default Value nor Value Generation must be supplied. The Field tables in the Interface section list them under **Required**.

```python
from model.interface import Broker

try:
    Broker(name="FxPro")
except ValueError as error:
    print(str(error).splitlines()[:2])
print(Broker(name="FxPro", user_id=1).name)
```

```text
['1 validation error for Broker', 'user_id']
FxPro
```

### A Field name is not recognized

Only the Fields an Entity declares are accepted, and a misspelled or extra name is rejected instead of being ignored.

```python
from model.interface import Broker

try:
    Broker(name="FxPro", user_id=1, colour="red")
except ValueError as error:
    print(str(error).splitlines()[:2])
print(Broker(name="FxPro", user_id=1).name)
```

```text
['1 validation error for Broker', 'colour']
FxPro
```

### The identity cannot be changed

An identity cannot change once it has been assigned or generated. Create a new Entity to refer to a different identity.

```python
from model.interface import Broker

broker = Broker(name="FxPro", user_id=1, id=5)
try:
    broker.id = 6
except ValueError as error:
    print(error)
print(broker.id)
print(Broker(name="FxPro", user_id=1, id=6).id)
```

```text
Broker.id is immutable
5
6
```

### JSON is rejected when it is built

Decimal and datetime values must be encoded as strings in JSON. A decimal string must be a base-10 number and a datetime string an ISO 8601 date-time; a JSON number is not accepted for a decimal.

```python
from model.interface import TrailingRule

document = {"name": "Breakeven", "trailing_group_id": 1, "trigger_percentage": 50.5}
try:
    TrailingRule.from_json(document)
except TypeError as error:
    print(error)
document["trigger_percentage"] = "50.5"
print(TrailingRule.from_json(document).trigger_percentage)
```

```text
Trailing Rule.trigger_percentage: decimal must be encoded as a string
50.5
```

### Installation reports an unsupported Python version

Model requires Python 3.14 or later. Install a supported interpreter, for example with `uv python install 3.14`, and run `uv sync` again.

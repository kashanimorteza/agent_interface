# Model

## Overview

Model is the reusable data library of the Trading Assistant. It defines the application's 15 data Entities once, in a technology-independent form, and publishes them through one Interface. Every Entity validates its own values strictly, converts to and from JSON text without loss, and exposes its complete public meaning as a Declaration.

```python
from model.interface import User

user = User(name="Ada", username="ada", password="placeholder", api_key="placeholder")
print(user.is_active)  # True: the default declared for the Field
print(user.id)  # None: pending until storage assigns it
```

## Interface

The Interface is the module `model.interface`. It publishes two things and nothing else:

- **Entity Exports** — every Entity on its own, by its own name.
- **Entity Collection** — `entities`, an immutable tuple of every Entity, once each, in the order listed below.

Import one Entity directly when you work with that Entity:

```python
from model.interface import Account

print(Account.declaration.name)
```

Enumerate the collection when you work with all Entities without knowing their names:

```python
from model.interface import entities

for entity in entities:
    print(entity.declaration.name, len(entity.declaration.fields))
```

Each Entity below is listed in the order of the collection with its description, its complete Field table, and its Entity Metadata.

### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `name` | `string` | no | none | none | no | none | none | The user's display name. |
| `username` | `string` | no | none | none | no | none | none | The username used to identify the user. |
| `password` | `string` | no | none | none | no | none | none | The password credential used by the user. |
| `api_key` | `string` | no | none | none | no | none | none | The API key assigned to the user. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the user is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the user. |

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** (`name`); (`username`)
- **Indexes:** none

### Trading Platform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `name` | `string` | no | none | none | no | none | none | The platform's display name. |
| `code` | `string` | no | none | none | no | none | none | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the platform is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the platform. |

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** (`name`)
- **Indexes:** none

### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `user_id` | `integer` | no | none | none | no | none | none | Identifies the user who owns this instance. |
| `trading_platform_id` | `integer` | no | none | none | no | none | none | Identifies the trading platform used by this instance. |
| `name` | `string` | no | none | none | no | none | none | The instance's display name. |
| `ip` | `string` | yes | none | none | no | none | none | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | `string` | yes | none | none | no | none | none | Defines the technical username used to establish the Instance connection when required. |
| `password` | `string` | yes | none | none | no | none | none | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | `string` | yes | none | none | no | none | none | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the instance is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the instance. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`; `trading_platform_id` → Trading Platform.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `user_id` | `integer` | no | none | none | no | none | none | Identifies the user who owns this currency. |
| `code` | `string` | no | none | none | no | 3 | none | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | `string` | yes | none | none | no | none | none | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | `string` | yes | none | none | no | none | none | Identifies the country or region associated with the currency. |
| `decimal_digits` | `integer` | no | `2` | none | no | none | none | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the currency is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the currency. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `code`)
- **Indexes:** none

### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `name` | `string` | no | none | none | no | none | none | The broker's display name. |
| `user_id` | `integer` | no | none | none | no | none | none | Identifies the user who owns the broker configuration. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the broker is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the broker. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `broker_id` | `integer` | no | none | none | no | none | none | Identifies the broker that provides this asset. |
| `symbol` | `string` | no | none | none | no | none | none | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | `string` | no | none | none | no | none | none | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | `float` | no | `0.0` | none | no | none | none | Stores the size of one point for the asset. |
| `digits` | `integer` | no | `0` | none | no | none | none | Stores the number of decimal digits used for the asset's price. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the asset is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the asset. |

- **Primary Key:** `id`
- **Relations:** `broker_id` → Broker.`id`
- **Uniqueness Constraints:** (`broker_id`, `symbol`)
- **Indexes:** none

### Account Group

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `user_id` | `integer` | no | none | none | no | none | none | Identifies the user who owns the account group. |
| `name` | `string` | no | none | none | no | none | none | The account group's display name. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the account group is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the account group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `name` | `string` | no | none | none | no | none | none | The account's display name. |
| `group_id` | `integer` | no | none | none | no | none | none | Identifies the account group that contains the account. |
| `broker_id` | `integer` | no | none | none | no | none | none | Identifies the broker that owns the account. |
| `instance_id` | `integer` | no | none | none | no | none | none | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | `integer` | no | none | none | no | none | none | Identifies the base currency used by the account. |
| `username` | `string` | no | none | none | no | none | none | The username identifier used to access the trading account. |
| `password` | `string` | no | none | none | no | none | none | The credential used to access the trading account. |
| `leverage` | `integer` | no | none | none | no | none | none | Defines the account's leverage multiplier. |
| `balance` | `decimal` | no | `0` | none | no | none | none | Stores the account's current balance. |
| `account_type` | `string` | no | none | none | no | none | none | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the account is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the account. |

- **Primary Key:** `id`
- **Relations:** `group_id` → Account Group.`id`; `broker_id` → Broker.`id`; `instance_id` → Instance.`id`; `base_currency_id` → Currency.`id`
- **Uniqueness Constraints:** (`name`); (`group_id`, `broker_id`, `instance_id`)
- **Indexes:** none

### Trailing Group

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `user_id` | `integer` | no | none | none | no | none | none | Identifies the user who owns the trailing group. |
| `name` | `string` | no | none | none | no | none | none | The trailing group's display name. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the trailing group is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the trailing group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Trailing Rule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `name` | `string` | no | none | none | no | none | none | The trailing rule's display name. |
| `trailing_group_id` | `integer` | no | none | none | no | none | none | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | `decimal` | no | none | none | no | none | none | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | `decimal` | yes | none | none | no | none | none | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | `decimal` | yes | none | none | no | none | none | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the trailing rule is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the trailing rule. |

- **Primary Key:** `id`
- **Relations:** `trailing_group_id` → Trailing Group.`id`
- **Uniqueness Constraints:** (`name`); (`trailing_group_id`, `trigger_percentage`)
- **Indexes:** none

### Partial Group

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `user_id` | `integer` | no | none | none | no | none | none | Identifies the user who owns the partial group. |
| `name` | `string` | no | none | none | no | none | none | The partial group's display name. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the partial group is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the partial group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Partial Rule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `name` | `string` | no | none | none | no | none | none | The partial rule's display name. |
| `partial_group_id` | `integer` | no | none | none | no | none | none | Identifies the partial group that contains the rule. |
| `profit_percentage` | `decimal` | no | none | none | no | none | none | Defines the profit percentage that activates the rule. |
| `close_percentage` | `decimal` | no | none | none | no | none | none | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the partial rule is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the partial rule. |

- **Primary Key:** `id`
- **Relations:** `partial_group_id` → Partial Group.`id`
- **Uniqueness Constraints:** (`name`); (`partial_group_id`, `profit_percentage`)
- **Indexes:** none

### Action Group

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `user_id` | `integer` | no | none | none | no | none | none | Identifies the user who owns the action group. |
| `name` | `string` | no | none | none | no | none | none | The action group's display name. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the action group is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the action group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Action

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `name` | `string` | no | none | none | no | none | none | The action's display name. |
| `action_group_id` | `integer` | no | none | none | no | none | none | Identifies the action group that contains the action. |
| `asset_id` | `integer` | no | none | none | no | none | none | Identifies the asset traded by the action. |
| `account_id` | `integer` | no | none | none | no | none | none | Identifies the account used to execute the action. |
| `partial_group_id` | `integer` | no | none | none | no | none | none | Identifies the Partial Group used by the action. |
| `trailing_group_id` | `integer` | no | none | none | no | none | none | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | `decimal` | no | none | none | no | none | none | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | `decimal` | no | none | none | no | none | none | Defines the Take Profit value used by the action. |
| `stop_loss` | `decimal` | no | none | none | no | none | none | Defines the Stop Loss value used by the action. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the action is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the action. |

- **Primary Key:** `id`
- **Relations:** `action_group_id` → Action Group.`id`; `asset_id` → Asset.`id`; `account_id` → Account.`id`; `partial_group_id` → Partial Group.`id`; `trailing_group_id` → Trailing Group.`id`
- **Uniqueness Constraints:** (`action_group_id`, `name`)
- **Indexes:** none

### Position

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Nullable | Default | Value Generation | Immutable | Size | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | `auto_increment` | yes | none | none | none |
| `user_id` | `integer` | no | none | none | no | none | none | Identifies the user who owns the position. |
| `name` | `string` | no | none | none | no | none | none | The position's display name. |
| `trading_platform_id` | `integer` | no | none | none | no | none | none | Identifies the trading platform used to execute the position. |
| `broker_id` | `integer` | no | none | none | no | none | none | Identifies the broker through which the position is executed. |
| `account_id` | `integer` | no | none | none | no | none | none | Identifies the trading account used for the position. |
| `trailing_group_id` | `integer` | no | none | none | no | none | none | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | `integer` | no | none | none | no | none | none | Identifies the Partial Group applied to the position. |
| `action_group_id` | `integer` | no | none | none | no | none | none | Identifies the Action Group associated with the position. |
| `action_id` | `integer` | no | none | none | no | none | none | Identifies the action from which the position is created. |
| `date` | `datetime` | no | none | none | no | none | none | Stores the position's date and time. |
| `volume` | `decimal` | no | none | none | no | none | none | Stores the position's trading volume. |
| `profit` | `decimal` | no | `0` | none | no | none | none | Stores the position's current profit or loss. |
| `is_executed` | `boolean` | no | `false` | none | no | none | none | Indicates whether the position has been executed. |
| `order_type` | `string` | no | none | none | no | none | none | Stores the position's order type. |
| `base_tp` | `decimal` | no | none | none | no | none | none | Stores the position's initial Take Profit value. |
| `base_sl` | `decimal` | no | none | none | no | none | none | Stores the position's initial Stop Loss value. |
| `real_tp` | `decimal` | no | none | none | no | none | none | Stores the position's current Take Profit value. |
| `real_sl` | `decimal` | no | none | none | no | none | none | Stores the position's current Stop Loss value. |
| `is_active` | `boolean` | no | `true` | none | no | none | none | Indicates whether the position is active. |
| `description` | `string` | yes | none | none | no | none | none | Describes the position. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`; `trading_platform_id` → Trading Platform.`id`; `broker_id` → Broker.`id`; `account_id` → Account.`id`; `trailing_group_id` → Trailing Group.`id`; `partial_group_id` → Partial Group.`id`; `action_group_id` → Action Group.`id`; `action_id` → Action.`id`
- **Uniqueness Constraints:** (`name`)
- **Indexes:** none

## Declaration

Every Entity carries its complete public meaning as a read-only `declaration` attribute of the Entity itself. A Declaration is an immutable record; it holds no behaviour.

```python
from model.interface import Instance

declaration = Instance.declaration

print(declaration.name, "-", declaration.description)

for field in declaration.fields:
    print(
        field.name,
        field.type.value,
        field.nullable,
        field.default,
        field.value_generation,
    )

print(declaration.primary_key)

for relation in declaration.relations:
    print(relation.local_field, "->", relation.target_entity, relation.target_field)

print(declaration.unique_constraints)
print(declaration.indexes)
```

A Declaration exposes `name`, `description`, `fields`, `primary_key`, `relations`, `unique_constraints` and `indexes`. A Field Declaration exposes `name`, `type`, `nullable`, `description`, `default`, `sensitivity`, `immutable`, `constraints` and `value_generation`. A Field with no stated Default Value has `default` equal to `NO_DEFAULT`, which differs from an explicit `None` default.

## Foundation

Foundation is the shared public contract every Entity extends. It gives each Entity conversion to and from JSON text, and nothing else.

`to_json` returns JSON text with one root object whose keys are exactly the Field names, in Declaration order. A decimal is written as exact text, a datetime as an ISO 8601 string with its offset, a uuid as text, and a value not yet generated as `null`.

```python
from model.interface import User

user = User(name="Ada", username="ada", password="placeholder", api_key="placeholder")
print(user.to_json())
```

`from_json` rebuilds an Entity from such text under the same rules as direct construction. It rejects malformed text, a repeated key, a non-standard constant such as `NaN`, a root that is not one object, an unknown key, a missing required key, and a value of the wrong form. A `null` identity is read as not yet generated; any other identity value is refused, like a value supplied directly.

```python
from model.interface import User

text = '{"id": null, "name": "Ada", "username": "ada", "password": "placeholder", "api_key": "placeholder", "is_active": true, "description": null}'
user = User.from_json(text)
print(user.name)
```

A complete round trip: an Entity to JSON text and back to an equal Entity, with exact decimal and timezone-aware datetime values.

```python
from datetime import UTC, datetime
from decimal import Decimal

from model.interface import Position

position = Position(
    user_id=1,
    name="Position-1",
    trading_platform_id=1,
    broker_id=1,
    account_id=1,
    trailing_group_id=1,
    partial_group_id=1,
    action_group_id=1,
    action_id=1,
    date=datetime(2024, 1, 2, 3, 4, 5, tzinfo=UTC),
    volume=Decimal("0.10"),
    order_type="market",
    base_tp=Decimal("1.2500"),
    base_sl=Decimal("1.1500"),
    real_tp=Decimal("1.2500"),
    real_sl=Decimal("1.1500"),
)

text = position.to_json()
restored = Position.from_json(text)

assert restored == position
assert restored.volume == Decimal("0.10")
assert restored.date == position.date
assert restored.to_json() == text
```

## Setup

Model is a Python library managed with [uv](https://docs.astral.sh/uv/). It needs Python 3.14 or newer.

1. Open the Model directory.
2. Install the locked dependencies into an isolated environment:

   ```bash
   uv sync
   ```

3. Confirm the Interface loads:

   ```bash
   uv run python -c "import model.interface"
   ```

Another Component of this project uses Model as a local path dependency on this directory, never from a package index. In the consumer's `pyproject.toml`:

```toml
[project]
dependencies = ["model"]

[tool.uv.sources]
model = { path = "../model" }
```

## Use

Create an Entity from its Field values. A value must already be of the declared Type; nothing is coerced, and an undeclared Field is refused.

```python
from model.interface import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(currency.decimal_digits)  # 2: the declared default
```

Assign a mutable Field. The whole Entity is validated first, so a refused assignment keeps the previous value; an immutable Field cannot be assigned.

```python
from model.interface import Currency

currency = Currency(user_id=1, code="USD")
currency.symbol = "$"

try:
    currency.code = "TOOLONG"
except ValueError:
    print(currency.code)  # USD
```

An Entity is not hashable. Compare Entities by value, and index them by a Field value instead.

Work with all Entities through the collection, for example to read every Declaration:

```python
from model.interface import entities

for entity in entities:
    declaration = entity.declaration
    print(declaration.name, [field.name for field in declaration.fields])
```

Every Entity's table form is registered in one shared table metadata that you reach through the Entities themselves. It contains exactly the Model tables. Model only declares this form and never creates or queries storage.

```python
from model.interface import entities

metadata = entities[0].metadata
print(sorted(metadata.tables))
```

## Verify

Run the script below from the Model directory with `uv run python`. It checks, using only the Interface, the Declarations and the Entities themselves: the exact set of exports, the order and membership of the collection and its correspondence with the exports, that exports and collection items are the actual Entities, each exposing its own actual Declaration, immutability, that loading has no side effect, representative construction and its refusals, Declaration access, the storage form of every Entity, and a lossless JSON round trip. It prints `Model verified` when every check holds.

```python
import os
import subprocess
import sys
import tempfile
from dataclasses import FrozenInstanceError
from datetime import UTC, date, datetime, time
from decimal import Decimal
from uuid import uuid4

import model.interface as interface
from model.core.declaration import NO_DEFAULT, DeclarationError, FieldDeclaration
from model.interface import entities

EXPECTED = [
    "User",
    "TradingPlatform",
    "Instance",
    "Currency",
    "Broker",
    "Asset",
    "AccountGroup",
    "Account",
    "TrailingGroup",
    "TrailingRule",
    "PartialGroup",
    "PartialRule",
    "ActionGroup",
    "Action",
    "Position",
]
SAMPLES = {
    "string": "x",
    "integer": 1,
    "float": 1.5,
    "decimal": Decimal("1.50"),
    "boolean": True,
    "datetime": datetime(2024, 1, 2, 3, 4, 5, tzinfo=UTC),
    "date": date(2024, 1, 2),
    "time": time(1, 2, 3),
    "uuid": uuid4(),
}


def refused(action, *errors):
    try:
        action()
    except errors:
        return True
    return False


def valid_values(entity):
    return {
        field.name: "A" * field.constraints.size
        if field.constraints.size
        else SAMPLES[field.type.value]
        for field in entity.declaration.fields
        if field.default is NO_DEFAULT
        and not field.nullable
        and field.value_generation is None
    }


# Interface: exactly the Entity exports and the collection, in Target order.
assert sorted(name for name in vars(interface) if not name.startswith("_")) == sorted(
    [*EXPECTED, "entities"]
)
assert isinstance(entities, tuple)
assert [entity.__name__ for entity in entities] == EXPECTED
assert all(getattr(interface, entity.__name__) is entity for entity in entities)

# Loading has no side effect: a fresh interpreter in an empty directory creates nothing.
with tempfile.TemporaryDirectory() as directory:
    done = subprocess.run(
        [sys.executable, "-c", "import model.interface"],
        cwd=directory,
        capture_output=True,
    )
    assert done.returncode == 0 and not done.stdout and not os.listdir(directory)

# A Type outside the closed set stops generation.
assert refused(lambda: FieldDeclaration("x", "bogus", False), DeclarationError)

for entity in entities:
    declaration = entity.declaration
    names = [field.name for field in declaration.fields]

    # Declaration: the Entity's own actual Declaration, never a copy or an inherited one.
    assert "declaration" in vars(entity) and declaration is vars(entity)["declaration"]

    # Declaration: immutable, with the mandatory Fields.
    assert refused(lambda: setattr(declaration, "name", "Other"), FrozenInstanceError)
    assert declaration.primary_key == "id"
    assert next(f for f in declaration.fields if f.name == "id").immutable
    assert (
        next(f for f in declaration.fields if f.name == "is_active").type.value
        == "boolean"
    )

    # Construction, and its refusals.
    values = valid_values(entity)
    instance = entity(**values)
    assert instance.id is None and instance.is_active is True
    assert refused(lambda: entity(**values, unknown=1), ValueError)
    assert refused(lambda: entity(**{**values, "id": 1}), ValueError)
    assert refused(lambda: setattr(instance, "id", 1), ValueError)
    for name in values:
        assert refused(lambda: entity(**{**values, name: object()}), ValueError)
        assert refused(
            lambda: entity(**{k: v for k, v in values.items() if k != name}), ValueError
        )

    # Lossless JSON round trip with keys in Declaration order.
    text = instance.to_json()
    assert list(__import__("json").loads(text)) == names
    assert (
        entity.from_json(text) == instance and entity.from_json(text).to_json() == text
    )

    # Storage form: names, keys, constraints, indexes and identity column.
    table = entity.__table__
    assert table.name == entity.__name__ and [c.name for c in table.columns] == names
    assert table.c.id.primary_key and table.c.id.identity is not None
    unique = {
        tuple(c.name for c in k.columns): k.name
        for k in table.constraints
        if k.__class__.__name__ == "UniqueConstraint"
    }
    for entry in declaration.unique_constraints:
        assert unique[entry] == f"uq_{table.name}_{'_'.join(entry)}"
    for relation in declaration.relations:
        key = next(iter(table.c[relation.local_field].foreign_keys))
        assert key.constraint.name == f"fk_{table.name}_{relation.local_field}"
        assert key.column.name == relation.target_field

assert sorted(entities[0].metadata.tables) == sorted(EXPECTED)
print("Model verified")
```

Quality checks for the source use the tools declared in the Model dependency groups:

```bash
uv run ruff format --check
uv run ruff check
uv run ty check
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'model'`** — the library is not installed in the interpreter you are using. Run commands through `uv run` inside the Model directory, or declare Model as a local path dependency in the consumer.
- **`ValidationError` mentioning a Type, such as "Input should be a valid string"** — Model never coerces. Pass a value that is already of the declared Type, for example a `decimal.Decimal` for a decimal Field and a timezone-aware `datetime` for a datetime Field.
- **`ValidationError` "Extra inputs are not permitted"** — the name is not a Field of the Entity. Check `Entity.declaration.fields`.
- **`ValueError: The Field 'id' is generated by storage and cannot be supplied.`** — an Auto Increment Field cannot be given a value, including `None`. Omit it; it stays pending until storage assigns it. For the same reason `from_json` refuses a non-null `id`.
- **`ValueError: The Field 'id' cannot be assigned.`** — an immutable Field cannot be assigned after creation.
- **`TypeError: unhashable type`** — Entities are mutable and are not hashable. Use a Field value, such as the identity, as the key.
- **`<redacted>` in a validation message** — the input belongs to a Field with a Sensitivity Marker, so its value is hidden on purpose.
- **`DeclarationError` when an Entity module loads** — the Entity type does not match its Declaration: its type or table name is not the physical name of the Entity, its Fields differ from the Declaration's Fields or their order, a Field name cannot be used, or another Entity already uses the physical name. Correct the Entity or its Declaration.
- **`DeclarationError` when creating a Declaration** — the Declaration is invalid or contradictory, for example a Default Value together with Value Generation, a size on a non-string Field, or a Relation naming an unknown Field. Fix the named item; Model never repairs a Declaration.

# Model

Model defines and publishes the application's data-model Entities and their complete public meaning. Every Entity is a flat, validated record with its own public Declaration and a lossless conversion to and from JSON text.

## Overview

Each Entity carries its Fields, its metadata (Primary Key, Relations, Uniqueness Constraints, Indexes) and a Declaration that states them. Entities validate strictly: nothing is coerced, undeclared Fields are refused, and a failed assignment keeps the prior value. Every Entity also has a table-ready form, so a consumer that stores data creates the Tables from the Entities themselves; Model never stores anything.

```python
from model import User

user = User(name="Admin", username="admin", password="placeholder", api_key="placeholder")
print(user.to_json())
```

```text
{"id": null, "name": "Admin", "username": "admin", "password": "placeholder", "api_key": "placeholder", "is_active": true, "description": null}
```

The pending `id` is `null` until storage assigns it.

## Interface

Interface contract version: `2.1`.

The package root publishes exactly two things:

- **Entity Exports** — every Entity on its own, by its own name, for a consumer that works with one specific Entity.
- **Entity Collection** — `entities`, an immutable tuple of every Entity once, in the order below, for a consumer that works with all Entities without knowing their names. Each item is the same object as its export.

Importing the package creates no Entity instance, data, connection, file or process.

Import one Entity directly:

```python
from model import Account

account = Account(
    name="Acc-1",
    group_id=1,
    broker_id=1,
    instance_id=1,
    base_currency_id=1,
    username="placeholder",
    password="placeholder",
    leverage=100,
    account_type="CFD",
)
print(type(account).__name__, account.leverage)
```

```text
Account 100
```

Enumerate the Collection:

```python
from model import entities

for entity in entities:
    print(entity.declaration.name, len(entity.declaration.fields))
```

```text
User 7
Trading Platform 5
Instance 10
Currency 8
Broker 5
Asset 8
Account Group 5
Account 13
Trailing Group 5
Trailing Rule 8
Partial Group 5
Partial Rule 7
Action Group 5
Action 12
Position 21
```

### Entities

The Entities, in Collection order. Field tables list every property of each Field Declaration; metadata is listed beneath each table.

#### User

Exported as `User`.

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `name` | string | no | — | no | — | — | — | The user's display name. |
| `username` | string | no | — | no | — | — | — | The username used to identify the user. |
| `password` | string | no | — | no | password | — | — | The password credential used by the user. |
| `api_key` | string | no | — | no | sensitive | — | — | The API key assigned to the user. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the user is active. |
| `description` | string | yes | — | no | — | — | — | Describes the user. |

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:**
  - `name`
  - `username`
- **Indexes:** none

#### Trading Platform

Exported as `TradingPlatform`.

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `name` | string | no | — | no | — | — | — | The platform's display name. |
| `code` | string | no | — | no | — | — | — | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the platform is active. |
| `description` | string | yes | — | no | — | — | — | Describes the platform. |

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:**
  - `name`
- **Indexes:** none

#### Instance

Exported as `Instance`.

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `user_id` | integer | no | — | no | — | — | — | Identifies the user who owns this instance. |
| `trading_platform_id` | integer | no | — | no | — | — | — | Identifies the trading platform used by this instance. |
| `name` | string | no | — | no | — | — | — | The instance's display name. |
| `ip` | string | yes | — | no | — | — | — | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | string | yes | — | no | — | — | — | Defines the technical username used to establish the Instance connection when required. |
| `password` | string | yes | — | no | password | — | — | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | string | yes | — | no | sensitive | — | — | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the instance is active. |
| `description` | string | yes | — | no | — | — | — | Describes the instance. |

- **Primary Key:** `id`
- **Relations:**
  - `user_id` → User.`id`
  - `trading_platform_id` → Trading Platform.`id`
- **Uniqueness Constraints:**
  - `user_id`, `name`
- **Indexes:** none

#### Currency

Exported as `Currency`.

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `user_id` | integer | no | — | no | — | — | — | Identifies the user who owns this currency. |
| `code` | string | no | — | no | — | 3 | — | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | string | yes | — | no | — | — | — | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | string | yes | — | no | — | — | — | Identifies the country or region associated with the currency. |
| `decimal_digits` | integer | no | `2` | no | — | — | — | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the currency is active. |
| `description` | string | yes | — | no | — | — | — | Describes the currency. |

- **Primary Key:** `id`
- **Relations:**
  - `user_id` → User.`id`
- **Uniqueness Constraints:**
  - `user_id`, `code`
- **Indexes:** none

#### Broker

Exported as `Broker`.

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `name` | string | no | — | no | — | — | — | The broker's display name. |
| `user_id` | integer | no | — | no | — | — | — | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the broker is active. |
| `description` | string | yes | — | no | — | — | — | Describes the broker. |

- **Primary Key:** `id`
- **Relations:**
  - `user_id` → User.`id`
- **Uniqueness Constraints:**
  - `user_id`, `name`
- **Indexes:** none

#### Asset

Exported as `Asset`.

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `broker_id` | integer | no | — | no | — | — | — | Identifies the broker that provides this asset. |
| `symbol` | string | no | — | no | — | — | — | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | string | no | — | no | — | — | — | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | float | no | `0.0` | no | — | — | — | Stores the size of one point for the asset. |
| `digits` | integer | no | `0` | no | — | — | — | Stores the number of decimal digits used for the asset's price. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the asset is active. |
| `description` | string | yes | — | no | — | — | — | Describes the asset. |

- **Primary Key:** `id`
- **Relations:**
  - `broker_id` → Broker.`id`
- **Uniqueness Constraints:**
  - `broker_id`, `symbol`
- **Indexes:** none

#### Account Group

Exported as `AccountGroup`.

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `user_id` | integer | no | — | no | — | — | — | Identifies the user who owns the account group. |
| `name` | string | no | — | no | — | — | — | The account group's display name. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the account group is active. |
| `description` | string | yes | — | no | — | — | — | Describes the account group. |

- **Primary Key:** `id`
- **Relations:**
  - `user_id` → User.`id`
- **Uniqueness Constraints:**
  - `user_id`, `name`
- **Indexes:** none

#### Account

Exported as `Account`.

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `name` | string | no | — | no | — | — | — | The account's display name. |
| `group_id` | integer | no | — | no | — | — | — | Identifies the account group that contains the account. |
| `broker_id` | integer | no | — | no | — | — | — | Identifies the broker that owns the account. |
| `instance_id` | integer | no | — | no | — | — | — | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | no | — | no | — | — | — | Identifies the base currency used by the account. |
| `username` | string | no | — | no | — | — | — | The username identifier used to access the trading account. |
| `password` | string | no | — | no | password | — | — | The credential used to access the trading account. |
| `leverage` | integer | no | — | no | — | — | — | Defines the account's leverage multiplier. |
| `balance` | decimal | no | `Decimal('0')` | no | — | — | — | Stores the account's current balance. |
| `account_type` | string | no | — | no | — | — | — | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the account is active. |
| `description` | string | yes | — | no | — | — | — | Describes the account. |

- **Primary Key:** `id`
- **Relations:**
  - `group_id` → Account Group.`id`
  - `broker_id` → Broker.`id`
  - `instance_id` → Instance.`id`
  - `base_currency_id` → Currency.`id`
- **Uniqueness Constraints:**
  - `name`
  - `group_id`, `broker_id`, `instance_id`
- **Indexes:** none

#### Trailing Group

Exported as `TrailingGroup`.

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `user_id` | integer | no | — | no | — | — | — | Identifies the user who owns the trailing group. |
| `name` | string | no | — | no | — | — | — | The trailing group's display name. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the trailing group is active. |
| `description` | string | yes | — | no | — | — | — | Describes the trailing group. |

- **Primary Key:** `id`
- **Relations:**
  - `user_id` → User.`id`
- **Uniqueness Constraints:**
  - `user_id`, `name`
- **Indexes:** none

#### Trailing Rule

Exported as `TrailingRule`.

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `name` | string | no | — | no | — | — | — | The trailing rule's display name. |
| `trailing_group_id` | integer | no | — | no | — | — | — | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | decimal | no | — | no | — | — | — | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | decimal | yes | — | no | — | — | — | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | decimal | yes | — | no | — | — | — | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the trailing rule is active. |
| `description` | string | yes | — | no | — | — | — | Describes the trailing rule. |

- **Primary Key:** `id`
- **Relations:**
  - `trailing_group_id` → Trailing Group.`id`
- **Uniqueness Constraints:**
  - `name`
  - `trailing_group_id`, `trigger_percentage`
- **Indexes:** none

#### Partial Group

Exported as `PartialGroup`.

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `user_id` | integer | no | — | no | — | — | — | Identifies the user who owns the partial group. |
| `name` | string | no | — | no | — | — | — | The partial group's display name. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the partial group is active. |
| `description` | string | yes | — | no | — | — | — | Describes the partial group. |

- **Primary Key:** `id`
- **Relations:**
  - `user_id` → User.`id`
- **Uniqueness Constraints:**
  - `user_id`, `name`
- **Indexes:** none

#### Partial Rule

Exported as `PartialRule`.

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `name` | string | no | — | no | — | — | — | The partial rule's display name. |
| `partial_group_id` | integer | no | — | no | — | — | — | Identifies the partial group that contains the rule. |
| `profit_percentage` | decimal | no | — | no | — | — | — | Defines the profit percentage that activates the rule. |
| `close_percentage` | decimal | no | — | no | — | — | — | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the partial rule is active. |
| `description` | string | yes | — | no | — | — | — | Describes the partial rule. |

- **Primary Key:** `id`
- **Relations:**
  - `partial_group_id` → Partial Group.`id`
- **Uniqueness Constraints:**
  - `name`
  - `partial_group_id`, `profit_percentage`
- **Indexes:** none

#### Action Group

Exported as `ActionGroup`.

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `user_id` | integer | no | — | no | — | — | — | Identifies the user who owns the action group. |
| `name` | string | no | — | no | — | — | — | The action group's display name. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the action group is active. |
| `description` | string | yes | — | no | — | — | — | Describes the action group. |

- **Primary Key:** `id`
- **Relations:**
  - `user_id` → User.`id`
- **Uniqueness Constraints:**
  - `user_id`, `name`
- **Indexes:** none

#### Action

Exported as `Action`.

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `name` | string | no | — | no | — | — | — | The action's display name. |
| `action_group_id` | integer | no | — | no | — | — | — | Identifies the action group that contains the action. |
| `asset_id` | integer | no | — | no | — | — | — | Identifies the asset traded by the action. |
| `account_id` | integer | no | — | no | — | — | — | Identifies the account used to execute the action. |
| `partial_group_id` | integer | no | — | no | — | — | — | Identifies the Partial Group used by the action. |
| `trailing_group_id` | integer | no | — | no | — | — | — | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | decimal | no | — | no | — | — | — | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | decimal | no | — | no | — | — | — | Defines the Take Profit value used by the action. |
| `stop_loss` | decimal | no | — | no | — | — | — | Defines the Stop Loss value used by the action. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the action is active. |
| `description` | string | yes | — | no | — | — | — | Describes the action. |

- **Primary Key:** `id`
- **Relations:**
  - `action_group_id` → Action Group.`id`
  - `asset_id` → Asset.`id`
  - `account_id` → Account.`id`
  - `partial_group_id` → Partial Group.`id`
  - `trailing_group_id` → Trailing Group.`id`
- **Uniqueness Constraints:**
  - `action_group_id`, `name`
- **Indexes:** none

#### Position

Exported as `Position`.

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Nullable | Default | Immutable | Sensitivity | Size | Generation | Description |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | yes | — | — | auto_increment | — |
| `user_id` | integer | no | — | no | — | — | — | Identifies the user who owns the position. |
| `name` | string | no | — | no | — | — | — | The position's display name. |
| `trading_platform_id` | integer | no | — | no | — | — | — | Identifies the trading platform used to execute the position. |
| `broker_id` | integer | no | — | no | — | — | — | Identifies the broker through which the position is executed. |
| `account_id` | integer | no | — | no | — | — | — | Identifies the trading account used for the position. |
| `trailing_group_id` | integer | no | — | no | — | — | — | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | integer | no | — | no | — | — | — | Identifies the Partial Group applied to the position. |
| `action_group_id` | integer | no | — | no | — | — | — | Identifies the Action Group associated with the position. |
| `action_id` | integer | no | — | no | — | — | — | Identifies the action from which the position is created. |
| `date` | datetime | no | — | no | — | — | — | Stores the position's date and time. |
| `volume` | decimal | no | — | no | — | — | — | Stores the position's trading volume. |
| `profit` | decimal | no | `Decimal('0')` | no | — | — | — | Stores the position's current profit or loss. |
| `is_executed` | boolean | no | `False` | no | — | — | — | Indicates whether the position has been executed. |
| `order_type` | string | no | — | no | — | — | — | Stores the position's order type. |
| `base_tp` | decimal | no | — | no | — | — | — | Stores the position's initial Take Profit value. |
| `base_sl` | decimal | no | — | no | — | — | — | Stores the position's initial Stop Loss value. |
| `real_tp` | decimal | no | — | no | — | — | — | Stores the position's current Take Profit value. |
| `real_sl` | decimal | no | — | no | — | — | — | Stores the position's current Stop Loss value. |
| `is_active` | boolean | no | `True` | no | — | — | — | Indicates whether the position is active. |
| `description` | string | yes | — | no | — | — | — | Describes the position. |

- **Primary Key:** `id`
- **Relations:**
  - `user_id` → User.`id`
  - `trading_platform_id` → Trading Platform.`id`
  - `broker_id` → Broker.`id`
  - `account_id` → Account.`id`
  - `trailing_group_id` → Trailing Group.`id`
  - `partial_group_id` → Partial Group.`id`
  - `action_group_id` → Action Group.`id`
  - `action_id` → Action.`id`
- **Uniqueness Constraints:**
  - `name`
- **Indexes:** none

## Declaration

Every Entity exposes its Declaration as the class attribute `declaration`. An Entity Declaration has `name`, `description`, `fields`, `primary_key`, `relations`, `unique_constraints` and `indexes`; each Field Declaration has `name`, `type`, `nullable`, `description`, `default`, `sensitivity`, `immutable`, `constraints` and `value_generation`. A Field with no Default Value has `default` equal to `model.core.declaration.ABSENT`, which differs from an explicit `None`. Declarations are immutable.

```python
from model import Account

declaration = Account.declaration
print(declaration.name)
print([field.name for field in declaration.fields][:4])
print(declaration.primary_key)
for relation in declaration.relations:
    print(relation.local_field, "->", relation.target_entity, relation.target_field)
print(declaration.unique_constraints)
print(declaration.indexes)
field = declaration.fields[-3]
print(field.name, field.type.value, field.nullable, field.default, field.immutable)
```

```text
Account
['id', 'name', 'group_id', 'broker_id']
id
group_id -> Account Group id
broker_id -> Broker id
instance_id -> Instance id
base_currency_id -> Currency id
(('name',), ('group_id', 'broker_id', 'instance_id'))
()
account_type string False ABSENT False
```

## Foundation

Every Entity extends Foundation, which converts it to and from JSON text. The text has one root object whose keys are exactly the Entity's Field names, in Declaration order. A decimal and a uuid are JSON strings, a datetime, date and time are ISO 8601 strings, and `null`, `false`, `0` and `""` stay distinct. A pending Auto Increment `id` is `null`.

`to_json` returns the text of an Entity:

```python
from model import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(currency.to_json())
```

```text
{"id": null, "user_id": 1, "code": "USD", "symbol": "$", "country": "United States", "decimal_digits": 2, "is_active": true, "description": null}
```

`from_json` builds an Entity from text, with the same rules as direct construction. It refuses malformed text, a repeated key, a non-standard constant such as `NaN`, and a root that is not one object:

```python
from model import Currency

text = (
    '{"id": null, "user_id": 1, "code": "USD", "symbol": "$", '
    '"country": "United States", "decimal_digits": 2, '
    '"is_active": true, "description": null}'
)
currency = Currency.from_json(text)
print(currency.code, currency.decimal_digits)
```

```text
USD 2
```

A complete round trip — Entity to JSON text and back to an Entity — keeps decimal and datetime values exact:

```python
from datetime import UTC, datetime
from decimal import Decimal

from model import Position

position = Position(
    user_id=1,
    name="Example",
    trading_platform_id=1,
    broker_id=1,
    account_id=1,
    trailing_group_id=1,
    partial_group_id=1,
    action_group_id=1,
    action_id=1,
    date=datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC),
    volume=Decimal("0.10"),
    order_type="buy",
    base_tp=Decimal("1.2500"),
    base_sl=Decimal("1.1500"),
    real_tp=Decimal("1.2500"),
    real_sl=Decimal("1.1500"),
)
text = position.to_json()
restored = Position.from_json(text)
print(restored.volume, restored.date.isoformat())
print(restored.to_json() == text)
```

```text
0.10 2026-01-02T03:04:05+00:00
True
```

## Setup

1. Install [uv](https://docs.astral.sh/uv/).
2. From this directory, run `uv sync`. It creates the isolated environment and installs the dependencies recorded in `uv.lock`. Python 3.14 or newer is required.
3. A consumer inside this repository declares a local path dependency on this directory and imports from the package root.
4. To check the source, run `uv run ruff format --check model`, `uv run ruff check model` and `uv run ty check model`.

## Use

Use Model through the Entity Exports and the Entity Collection:

```python
from model import User, entities

user = User(name="Admin", username="admin", password="placeholder", api_key="placeholder")
user.is_active = False
print(user.is_active)

try:
    user.id = 5
except ValueError as error:
    print(error)

tables = entities[0].metadata.tables
print(len(tables), sorted(tables)[:3])
```

```text
False
id: the Field cannot be assigned
15 ['Account', 'AccountGroup', 'Action']
```

- Construct an Entity with keyword values only. Omit an Auto Increment `id`; storage assigns it.
- Assign a mutable Field to change it. `id` is immutable and cannot be assigned.
- Read an Entity's meaning from `Entity.declaration`.
- Reach the table metadata of all Entities through any Entity, such as `User.metadata`.

## Verify

The following script checks the Interface-contract-conformant shape, exact Entity Export membership, Collection membership and order and its correspondence with the Exports, that each export is the actual Entity exposing its actual Declaration, the immutability of `id` and of the Collection, representative construction, Declaration access and a lossless JSON text round trip.

```python
import json

import model
from model import entities

assert len(entities) == len(set(entities)), "each Entity appears once"
assert [e.__name__ for e in entities] == [e.declaration.name.replace(" ", "") for e in entities]
assert set(model.__all__) == {e.__name__ for e in entities} | {"entities"}
for entity in entities:
    assert getattr(model, entity.__name__) is entity, "export is the actual Entity"
    declaration = entity.declaration
    assert declaration.primary_key == "id"
    names = [field.name for field in declaration.fields]
    assert tuple(entity.model_fields) == tuple(names), "Fields match the Declaration"
    by_name = {field.name: field for field in declaration.fields}
    assert by_name["id"].immutable and not by_name["id"].nullable
    assert by_name["is_active"].type.value == "boolean"
    assert not by_name["is_active"].nullable and not by_name["is_active"].immutable
    try:
        entity(unknown_field=1)
    except Exception:
        pass
    else:
        raise AssertionError("an undeclared Field is refused")
assert isinstance(entities, tuple), "the Collection cannot be modified"

user = model.User(name="Admin", username="admin", password="placeholder", api_key="placeholder")
text = user.to_json()
assert list(json.loads(text)) == [f.name for f in model.User.declaration.fields]
assert model.User.from_json(text).to_json() == text, "lossless round trip"
print("verified", len(entities), "Entities")
```

```text
verified 15 Entities
```

To verify that loading the package has no side effect, import it from an empty directory and confirm that nothing was created there:

```text
cd "$(mktemp -d)" && uv run --project <path to this directory> python -c "import model" && ls -A
```

The listing must be empty.

## Troubleshooting

- **`ValidationError` on construction or assignment** — a value broke a Field contract: wrong Type (nothing is coerced; a `bool` is not an integer, a `float` is not a decimal), a missing Required Field, an undeclared Field, a string over its size, a naive datetime, or a non-finite number. The message names the Field. The input of a Sensitivity-marked Field is replaced by `[hidden]`.
- **`ValueError: id: the value is generated and cannot be supplied`** — an Auto Increment `id` was passed, including `None`. Omit it. `from_json` therefore also refuses text that carries a non-null `id`.
- **`ValueError: id: the Field cannot be assigned`** — an immutable Field, or an Auto Increment Field, was assigned.
- **`TypeError` when importing an Entity** — the Entity's type name, table name or ordered Fields differ from its Declaration.
- **`ValueError` from a Declaration** — a Declaration is invalid or contradictory, for example an unknown Field Type, duplicate Field names, a default together with Value Generation, or a Relation naming an unknown local Field.
- **`TypeError: The JSON text must have one object at its root`** — `from_json` received valid JSON that is not one object.
- **`ValueError: ... is not a valid ... form`** — a decimal, uuid, datetime, date or time was not in its text form.

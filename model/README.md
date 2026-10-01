# Model

The Model is the reusable data library of the Trading Assistant. It defines 15 flat, technology-independent Entities and publishes each with its complete public meaning: its Fields, its Primary Key, its Relations, its Uniqueness Constraints, and its Indexes. Every Entity validates strictly, converts to and from JSON text without loss, and exposes its own Declaration.

## Overview

```python
from model.interface import User

user = User(
    name="Admin",
    username="admin",
    password="example-password",
    api_key="example-key",
)
print(user.username, user.is_active, user.id)
```

Output:

```text
admin True None
```

`is_active` defaults to `True`, and `id` stays `None` (pending) until the owner of storage assigns it.

## Interface

`model.interface` is the single public entrypoint. It publishes:

- **Entity Exports** — one explicit export per Entity, named by its physical name. A consumer that works with one Entity imports it directly and receives the actual Entity.
- **Entity Collection** — `entities`, one ordered, immutable tuple holding every Entity exactly once, in Target order. A consumer that works with all Entities enumerates it without knowing their names.

Importing one Entity directly:

```python
from model.interface import Position

print(Position.declaration.name)
```

Enumerating every Entity:

```python
from model.interface import entities

for entity in entities:
    print(entity.declaration.name)
```

Loading `model.interface` creates no Entity instance, data, connection, file, or process.

Entities in Target order:

1. `User`
2. `TradingPlatform`
3. `Instance`
4. `Currency`
5. `Broker`
6. `Asset`
7. `AccountGroup`
8. `Account`
9. `TrailingGroup`
10. `TrailingRule`
11. `PartialGroup`
12. `PartialRule`
13. `ActionGroup`
14. `Action`
15. `Position`

### Entities

#### User

Export: `User`

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `name` | string | no | none | none | none | no | none | The user's display name. |
| `username` | string | no | none | none | none | no | none | The username used to identify the user. |
| `password` | string | no | none | none | password | no | none | The password credential used by the user. |
| `api_key` | string | no | none | none | sensitive | no | none | The API key assigned to the user. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the user is active. |
| `description` | string | yes | none | none | none | no | none | Describes the user. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - none
- Uniqueness Constraints:
  - `name`
  - `username`
- Indexes:
  - none

#### Trading Platform

Export: `TradingPlatform`

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `name` | string | no | none | none | none | no | none | The platform's display name. |
| `code` | string | no | none | none | none | no | none | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the platform is active. |
| `description` | string | yes | none | none | none | no | none | Describes the platform. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - none
- Uniqueness Constraints:
  - `name`
- Indexes:
  - none

#### Instance

Export: `Instance`

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `user_id` | integer | no | none | none | none | no | none | Identifies the user who owns this instance. |
| `trading_platform_id` | integer | no | none | none | none | no | none | Identifies the trading platform used by this instance. |
| `name` | string | no | none | none | none | no | none | The instance's display name. |
| `ip` | string | yes | none | none | none | no | none | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | string | yes | none | none | none | no | none | Defines the technical username used to establish the Instance connection when required. |
| `password` | string | yes | none | none | password | no | none | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | string | yes | none | none | sensitive | no | none | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the instance is active. |
| `description` | string | yes | none | none | none | no | none | Describes the instance. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
  - `trading_platform_id` → `Trading Platform.id`
- Uniqueness Constraints:
  - `user_id, name`
- Indexes:
  - none

#### Currency

Export: `Currency`

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `user_id` | integer | no | none | none | none | no | none | Identifies the user who owns this currency. |
| `code` | string | no | none | size=3 | none | no | none | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | string | yes | none | none | none | no | none | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | string | yes | none | none | none | no | none | Identifies the country or region associated with the currency. |
| `decimal_digits` | integer | no | 2 | none | none | no | none | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the currency is active. |
| `description` | string | yes | none | none | none | no | none | Describes the currency. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
- Uniqueness Constraints:
  - `user_id, code`
- Indexes:
  - none

#### Broker

Export: `Broker`

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `name` | string | no | none | none | none | no | none | The broker's display name. |
| `user_id` | integer | no | none | none | none | no | none | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the broker is active. |
| `description` | string | yes | none | none | none | no | none | Describes the broker. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
- Uniqueness Constraints:
  - `user_id, name`
- Indexes:
  - none

#### Asset

Export: `Asset`

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `broker_id` | integer | no | none | none | none | no | none | Identifies the broker that provides this asset. |
| `symbol` | string | no | none | none | none | no | none | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | string | no | none | none | none | no | none | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | float | no | 0.0 | none | none | no | none | Stores the size of one point for the asset. |
| `digits` | integer | no | 0 | none | none | no | none | Stores the number of decimal digits used for the asset's price. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the asset is active. |
| `description` | string | yes | none | none | none | no | none | Describes the asset. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `broker_id` → `Broker.id`
- Uniqueness Constraints:
  - `broker_id, symbol`
- Indexes:
  - none

#### Account Group

Export: `AccountGroup`

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `user_id` | integer | no | none | none | none | no | none | Identifies the user who owns the account group. |
| `name` | string | no | none | none | none | no | none | The account group's display name. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the account group is active. |
| `description` | string | yes | none | none | none | no | none | Describes the account group. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
- Uniqueness Constraints:
  - `user_id, name`
- Indexes:
  - none

#### Account

Export: `Account`

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `name` | string | no | none | none | none | no | none | The account's display name. |
| `group_id` | integer | no | none | none | none | no | none | Identifies the account group that contains the account. |
| `broker_id` | integer | no | none | none | none | no | none | Identifies the broker that owns the account. |
| `instance_id` | integer | no | none | none | none | no | none | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | no | none | none | none | no | none | Identifies the base currency used by the account. |
| `username` | string | no | none | none | none | no | none | The username identifier used to access the trading account. |
| `password` | string | no | none | none | password | no | none | The credential used to access the trading account. |
| `leverage` | integer | no | none | none | none | no | none | Defines the account's leverage multiplier. |
| `balance` | decimal | no | Decimal('0') | none | none | no | none | Stores the account's current balance. |
| `account_type` | string | no | none | none | none | no | none | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the account is active. |
| `description` | string | yes | none | none | none | no | none | Describes the account. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `group_id` → `Account Group.id`
  - `broker_id` → `Broker.id`
  - `instance_id` → `Instance.id`
  - `base_currency_id` → `Currency.id`
- Uniqueness Constraints:
  - `name`
  - `group_id, broker_id, instance_id`
- Indexes:
  - none

#### Trailing Group

Export: `TrailingGroup`

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `user_id` | integer | no | none | none | none | no | none | Identifies the user who owns the trailing group. |
| `name` | string | no | none | none | none | no | none | The trailing group's display name. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the trailing group is active. |
| `description` | string | yes | none | none | none | no | none | Describes the trailing group. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
- Uniqueness Constraints:
  - `user_id, name`
- Indexes:
  - none

#### Trailing Rule

Export: `TrailingRule`

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `name` | string | no | none | none | none | no | none | The trailing rule's display name. |
| `trailing_group_id` | integer | no | none | none | none | no | none | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | decimal | no | none | none | none | no | none | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | decimal | yes | none | none | none | no | none | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | decimal | yes | none | none | none | no | none | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the trailing rule is active. |
| `description` | string | yes | none | none | none | no | none | Describes the trailing rule. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `trailing_group_id` → `Trailing Group.id`
- Uniqueness Constraints:
  - `name`
  - `trailing_group_id, trigger_percentage`
- Indexes:
  - none

#### Partial Group

Export: `PartialGroup`

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `user_id` | integer | no | none | none | none | no | none | Identifies the user who owns the partial group. |
| `name` | string | no | none | none | none | no | none | The partial group's display name. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the partial group is active. |
| `description` | string | yes | none | none | none | no | none | Describes the partial group. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
- Uniqueness Constraints:
  - `user_id, name`
- Indexes:
  - none

#### Partial Rule

Export: `PartialRule`

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `name` | string | no | none | none | none | no | none | The partial rule's display name. |
| `partial_group_id` | integer | no | none | none | none | no | none | Identifies the partial group that contains the rule. |
| `profit_percentage` | decimal | no | none | none | none | no | none | Defines the profit percentage that activates the rule. |
| `close_percentage` | decimal | no | none | none | none | no | none | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the partial rule is active. |
| `description` | string | yes | none | none | none | no | none | Describes the partial rule. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `partial_group_id` → `Partial Group.id`
- Uniqueness Constraints:
  - `name`
  - `partial_group_id, profit_percentage`
- Indexes:
  - none

#### Action Group

Export: `ActionGroup`

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `user_id` | integer | no | none | none | none | no | none | Identifies the user who owns the action group. |
| `name` | string | no | none | none | none | no | none | The action group's display name. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the action group is active. |
| `description` | string | yes | none | none | none | no | none | Describes the action group. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
- Uniqueness Constraints:
  - `user_id, name`
- Indexes:
  - none

#### Action

Export: `Action`

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `name` | string | no | none | none | none | no | none | The action's display name. |
| `action_group_id` | integer | no | none | none | none | no | none | Identifies the action group that contains the action. |
| `asset_id` | integer | no | none | none | none | no | none | Identifies the asset traded by the action. |
| `account_id` | integer | no | none | none | none | no | none | Identifies the account used to execute the action. |
| `partial_group_id` | integer | no | none | none | none | no | none | Identifies the Partial Group used by the action. |
| `trailing_group_id` | integer | no | none | none | none | no | none | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | decimal | no | none | none | none | no | none | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | decimal | no | none | none | none | no | none | Defines the Take Profit value used by the action. |
| `stop_loss` | decimal | no | none | none | none | no | none | Defines the Stop Loss value used by the action. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the action is active. |
| `description` | string | yes | none | none | none | no | none | Describes the action. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `action_group_id` → `Action Group.id`
  - `asset_id` → `Asset.id`
  - `account_id` → `Account.id`
  - `partial_group_id` → `Partial Group.id`
  - `trailing_group_id` → `Trailing Group.id`
- Uniqueness Constraints:
  - `action_group_id, name`
- Indexes:
  - none

#### Position

Export: `Position`

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Nullable | Default | Constraints | Sensitivity | Immutable | Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | none | none | none | yes | auto_increment | none |
| `user_id` | integer | no | none | none | none | no | none | Identifies the user who owns the position. |
| `name` | string | no | none | none | none | no | none | The position's display name. |
| `trading_platform_id` | integer | no | none | none | none | no | none | Identifies the trading platform used to execute the position. |
| `broker_id` | integer | no | none | none | none | no | none | Identifies the broker through which the position is executed. |
| `account_id` | integer | no | none | none | none | no | none | Identifies the trading account used for the position. |
| `trailing_group_id` | integer | no | none | none | none | no | none | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | integer | no | none | none | none | no | none | Identifies the Partial Group applied to the position. |
| `action_group_id` | integer | no | none | none | none | no | none | Identifies the Action Group associated with the position. |
| `action_id` | integer | no | none | none | none | no | none | Identifies the action from which the position is created. |
| `date` | datetime | no | none | none | none | no | none | Stores the position's date and time. |
| `volume` | decimal | no | none | none | none | no | none | Stores the position's trading volume. |
| `profit` | decimal | no | Decimal('0') | none | none | no | none | Stores the position's current profit or loss. |
| `is_executed` | boolean | no | False | none | none | no | none | Indicates whether the position has been executed. |
| `order_type` | string | no | none | none | none | no | none | Stores the position's order type. |
| `base_tp` | decimal | no | none | none | none | no | none | Stores the position's initial Take Profit value. |
| `base_sl` | decimal | no | none | none | none | no | none | Stores the position's initial Stop Loss value. |
| `real_tp` | decimal | no | none | none | none | no | none | Stores the position's current Take Profit value. |
| `real_sl` | decimal | no | none | none | none | no | none | Stores the position's current Stop Loss value. |
| `is_active` | boolean | no | True | none | none | no | none | Indicates whether the position is active. |
| `description` | string | yes | none | none | none | no | none | Describes the position. |

**Entity Metadata**

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
  - `trading_platform_id` → `Trading Platform.id`
  - `broker_id` → `Broker.id`
  - `account_id` → `Account.id`
  - `trailing_group_id` → `Trailing Group.id`
  - `partial_group_id` → `Partial Group.id`
  - `action_group_id` → `Action Group.id`
  - `action_id` → `Action.id`
- Uniqueness Constraints:
  - `name`
- Indexes:
  - none

## Declaration

Every Entity exposes its own public Declaration as the class attribute `declaration`. It is a frozen record: nothing in it can be changed.

```python
from model.interface import Account

declaration = Account.declaration
print(declaration.name, declaration.primary_key)
for field in declaration.fields[:4]:
    print(field.name, field.type, "null" if field.nullable else "not null")
print(declaration.relations[0])
print(declaration.unique_constraints)
print(declaration.indexes)
```

Output:

```text
Account id
id integer not null
name string not null
group_id integer not null
broker_id integer not null
Relation(local_field='group_id', target_entity='Account Group', target_field='id')
(('name',), ('group_id', 'broker_id', 'instance_id'))
()
```

- `Declaration` members: `name`, `description`, `fields`, `primary_key`, `relations`, `unique_constraints`, `indexes`.
- `FieldDeclaration` members: `name`, `description`, `type`, `nullable`, `has_default`, `default`, `sensitivity`, `immutable`, `constraints`, `value_generation`.
- `Relation` members: `local_field`, `target_entity`, `target_field`.
- `unique_constraints` and `indexes` are tuples of ordered Field-name tuples.

## Foundation

Every Entity carries the shared conversion capabilities. JSON text has one object at its root whose keys are the Entity's Fields in Declaration order. Decimal values and uuids are text, datetimes, dates, and times are ISO 8601 (datetimes keep their offset), and `null`, `false`, zero, and the empty string stay distinct.

`to_json` turns an Entity into JSON text:

```python
from model.interface import User

user = User(
    name="Admin",
    username="admin",
    password="example-password",
    api_key="example-key",
)
print(user.to_json())
```

```text
{"id": null, "name": "Admin", "username": "admin", "password": "example-password", "api_key": "example-key", "is_active": true, "description": null}
```

`from_json` rebuilds an Entity from JSON text under the same strict rules as direct construction:

```python
from model.interface import Broker

text = '{"id": null, "name": "Example Broker", "user_id": 1, "is_active": true, "description": null}'
broker = Broker.from_json(text)
print(broker.name, broker.is_active)
```

```text
Example Broker True
```

A complete round trip with exact decimal and datetime values:

```python
import datetime
import decimal

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
    date=datetime.datetime(2026, 1, 2, 3, 4, 5, tzinfo=datetime.timezone.utc),
    volume=decimal.Decimal("0.10"),
    order_type="buy",
    base_tp=decimal.Decimal("1.2"),
    base_sl=decimal.Decimal("0.9"),
    real_tp=decimal.Decimal("1.2"),
    real_sl=decimal.Decimal("0.9"),
)
text = position.to_json()
rebuilt = Position.from_json(text)
print(rebuilt == position, rebuilt.volume, rebuilt.date.isoformat())
```

```text
True 0.10 2026-01-02T03:04:05+00:00
```

The JSON text of that Position:

```json
{
  "id": null,
  "user_id": 1,
  "name": "Position-1",
  "trading_platform_id": 1,
  "broker_id": 1,
  "account_id": 1,
  "trailing_group_id": 1,
  "partial_group_id": 1,
  "action_group_id": 1,
  "action_id": 1,
  "date": "2026-01-02T03:04:05+00:00",
  "volume": "0.10",
  "profit": "0",
  "is_executed": false,
  "order_type": "buy",
  "base_tp": "1.2",
  "base_sl": "0.9",
  "real_tp": "1.2",
  "real_sl": "0.9",
  "is_active": true,
  "description": null
}
```

An Entity whose identity is still pending converts with `"id": null`. JSON text that carries an integer `id` rebuilds an Entity with that identity, because the owner of storage assigned it; direct construction never accepts one.

## Setup

The Model is a Python library managed with `uv`.

```bash
cd model
uv sync
```

This creates the project's virtual environment and installs the exact versions recorded in `uv.lock`. Run the examples with `uv run python`.

## Use

Construct Entities with keyword arguments. Construction accepts only declared Fields, applies defaults, and rejects anything invalid:

```python
from model.interface import Broker

broker = Broker(name="Example Broker", user_id=1)
broker.name = "Renamed Broker"      # a mutable Field: validated, then stored
broker.description = None           # a nullable Field accepts null
print(broker.name, broker.is_active)
```

```text
Renamed Broker True
```

Rejections raise `pydantic.ValidationError` (a `ValueError`) and never contain the supplied values:

```python
from model.interface import Currency

Currency(user_id=1, code="USDX")    # rejected: code is limited to 3 characters
Currency(user_id=1, code="USD", zzz=1)  # rejected: unknown Field
broker.id = 5                       # rejected: id is immutable
```

Enumerating all Entities uses the collection:

```python
from model.interface import entities

print(len(entities), [entity.declaration.name for entity in entities][:3])
```

```text
15 ['User', 'Trading Platform', 'Instance']
```

## Verify

The script below verifies the public surface. It prints `OK` when every check holds. Run it with `uv run python verify.py` after saving it from this page, or paste it into `uv run python`.

```python
import builtins
import dataclasses
import gc
import socket
import sqlite3
import subprocess

calls = []
real_open = builtins.open


def guarded_open(file, mode="r", *args, **kwargs):
    if any(flag in mode for flag in "wax+"):
        calls.append(("file write", str(file)))
    return real_open(file, mode, *args, **kwargs)


builtins.open = guarded_open
socket.socket.connect = lambda *args, **kwargs: calls.append(("network",))
sqlite3.connect = lambda *args, **kwargs: calls.append(("database",))
subprocess.Popen.__init__ = lambda *args, **kwargs: calls.append(("process",))

import model.interface as interface  # loading must have no side effect
from model.core.base import Entity

builtins.open = real_open

expected = [
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
public = [name for name in vars(interface) if not name.startswith("_")]

assert not calls, calls
assert not any(isinstance(obj, Entity) for obj in gc.get_objects())
assert sorted(public) == sorted(expected + ["entities"]), public
assert [entity.__name__ for entity in interface.entities] == expected
assert all(getattr(interface, name) is entity for name, entity in zip(expected, interface.entities))
assert isinstance(interface.entities, tuple)
assert all("declaration" in vars(entity) for entity in interface.entities)
assert all(
    dataclasses.is_dataclass(entity.declaration)
    and entity.declaration.__dataclass_params__.frozen
    for entity in interface.entities
)
assert not hasattr(interface, "__all__")

user = interface.User(name="a", username="b", password="c", api_key="d")
assert user.id is None and user.is_active is True
assert interface.User.from_json(user.to_json()) == user
for bad in ({"name": 1}, {"zzz": 1}, {"id": 7}):
    try:
        interface.User(**{"name": "a", "username": "b", "password": "c", "api_key": "d", **bad})
    except ValueError:
        pass
    else:
        raise AssertionError(bad)
try:
    user.id = 7
except ValueError:
    pass
else:
    raise AssertionError("id must be immutable")
print("OK")
```

## Troubleshooting

- **`ValidationError` when constructing or assigning** — the value does not satisfy the Field: wrong Type, null on a non-nullable Field, a value over the size limit, a missing required Field, or an unknown Field. The error names the Field and the rule, never the value.
- **`ValueError: ... is generated by its owner and cannot be supplied`** — identities are assigned by the owner of storage. Leave `id` out; it stays `None` until then.
- **`ValueError: ... is immutable`** — `id` cannot change once assigned.
- **`from_json` rejects the text** — the text must be one JSON object with only declared keys, each key once; decimals must be text such as `"1.50"`, not numbers; datetimes must carry an offset; `NaN` and `Infinity` are not valid JSON.
- **`ValueError: Entity differs from its Declaration` or `Invalid Model Metadata` while importing** — the listed Entity or Field no longer matches its Declaration, or a Relation target, Type, or name is unresolved. Each problem is listed with the item involved; importing stops so nothing is published half-built.
- **Decimal ordering in queries** — decimal columns store the exact decimal text so no precision is lost; text ordering is not numeric ordering, so compare decimals after reading them as `Decimal`.

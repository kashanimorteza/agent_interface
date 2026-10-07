# Model

## Overview

Model is the application's reusable data library. It defines each data concept of the Trading Assistant once, as a flat **Entity** whose public **Declaration** states its Fields, Relations and rules, and it publishes every Entity through one package entrypoint. An Entity validates its own values, converts to and from JSON text, and carries a table-ready form for storage. Model itself never runs storage.

```python
from model import User

user = User(
    name="Admin", username="admin", password="example-password", api_key="example-key"
)

print(user.is_active)  # True, the Activity Field default
print(user.id)  # None, the Identity stays pending until storage assigns it
print(user.to_json())
```

## Interface

The package root publishes exactly two forms, and nothing else. The Interface follows contract version 2.1.

- **Entity Exports** — every Entity on its own, imported by its own name, for a consumer that works with one specific Entity.
- **Entity Collection** — `entities`, every Entity once, in Target order, for a consumer that works with all Entities without knowing their names.

A consumer that needs another name gives it on its own side when it imports.

Import one Entity directly:

```python
from model import Account

print(Account.declaration.name)
```

Enumerate the Entity Collection:

```python
from model import entities

for entity in entities:
    print(entity.declaration.name)
```

The Entities, in Target order:

### User

Exported as `User`.

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `name` | string | false | — | — | false | — | — | The user's display name. |
| `username` | string | false | — | — | false | — | — | The username used to identify the user. |
| `password` | string | false | — | — | false | — | — | The password credential used by the user. |
| `api_key` | string | false | — | — | false | — | — | The API key assigned to the user. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the user is active. |
| `description` | string | true | — | — | false | — | — | Describes the user. |

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** (`name`); (`username`)
- **Indexes:** none

### Trading Platform

Exported as `TradingPlatform`.

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `name` | string | false | — | — | false | — | — | The platform's display name. |
| `code` | string | false | — | — | false | — | — | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the platform is active. |
| `description` | string | true | — | — | false | — | — | Describes the platform. |

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** (`name`)
- **Indexes:** none

### Instance

Exported as `Instance`.

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `user_id` | integer | false | — | — | false | — | — | Identifies the user who owns this instance. |
| `trading_platform_id` | integer | false | — | — | false | — | — | Identifies the trading platform used by this instance. |
| `name` | string | false | — | — | false | — | — | The instance's display name. |
| `ip` | string | true | — | — | false | — | — | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | string | true | — | — | false | — | — | Defines the technical username used to establish the Instance connection when required. |
| `password` | string | true | — | — | false | — | — | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | string | true | — | — | false | — | — | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the instance is active. |
| `description` | string | true | — | — | false | — | — | Describes the instance. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`; `trading_platform_id` → Trading Platform.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Currency

Exported as `Currency`.

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `user_id` | integer | false | — | — | false | — | — | Identifies the user who owns this currency. |
| `code` | string | false | — | — | false | size 3 | — | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | string | true | — | — | false | — | — | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | string | true | — | — | false | — | — | Identifies the country or region associated with the currency. |
| `decimal_digits` | integer | false | 2 | — | false | — | — | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the currency is active. |
| `description` | string | true | — | — | false | — | — | Describes the currency. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `code`)
- **Indexes:** none

### Broker

Exported as `Broker`.

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `name` | string | false | — | — | false | — | — | The broker's display name. |
| `user_id` | integer | false | — | — | false | — | — | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the broker is active. |
| `description` | string | true | — | — | false | — | — | Describes the broker. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Asset

Exported as `Asset`.

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `broker_id` | integer | false | — | — | false | — | — | Identifies the broker that provides this asset. |
| `symbol` | string | false | — | — | false | — | — | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | string | false | — | — | false | — | — | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | float | false | 0.0 | — | false | — | — | Stores the size of one point for the asset. |
| `digits` | integer | false | 0 | — | false | — | — | Stores the number of decimal digits used for the asset's price. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the asset is active. |
| `description` | string | true | — | — | false | — | — | Describes the asset. |

- **Primary Key:** `id`
- **Relations:** `broker_id` → Broker.`id`
- **Uniqueness Constraints:** (`broker_id`, `symbol`)
- **Indexes:** none

### Account Group

Exported as `AccountGroup`.

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `user_id` | integer | false | — | — | false | — | — | Identifies the user who owns the account group. |
| `name` | string | false | — | — | false | — | — | The account group's display name. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the account group is active. |
| `description` | string | true | — | — | false | — | — | Describes the account group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Account

Exported as `Account`.

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `name` | string | false | — | — | false | — | — | The account's display name. |
| `group_id` | integer | false | — | — | false | — | — | Identifies the account group that contains the account. |
| `broker_id` | integer | false | — | — | false | — | — | Identifies the broker that owns the account. |
| `instance_id` | integer | false | — | — | false | — | — | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | false | — | — | false | — | — | Identifies the base currency used by the account. |
| `username` | string | false | — | — | false | — | — | The username identifier used to access the trading account. |
| `password` | string | false | — | — | false | — | — | The credential used to access the trading account. |
| `leverage` | integer | false | — | — | false | — | — | Defines the account's leverage multiplier. |
| `balance` | decimal | false | Decimal('0') | — | false | — | — | Stores the account's current balance. |
| `account_type` | string | false | — | — | false | — | — | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the account is active. |
| `description` | string | true | — | — | false | — | — | Describes the account. |

- **Primary Key:** `id`
- **Relations:** `group_id` → Account Group.`id`; `broker_id` → Broker.`id`; `instance_id` → Instance.`id`; `base_currency_id` → Currency.`id`
- **Uniqueness Constraints:** (`name`); (`group_id`, `broker_id`, `instance_id`)
- **Indexes:** none

### Trailing Group

Exported as `TrailingGroup`.

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `user_id` | integer | false | — | — | false | — | — | Identifies the user who owns the trailing group. |
| `name` | string | false | — | — | false | — | — | The trailing group's display name. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the trailing group is active. |
| `description` | string | true | — | — | false | — | — | Describes the trailing group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Trailing Rule

Exported as `TrailingRule`.

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `name` | string | false | — | — | false | — | — | The trailing rule's display name. |
| `trailing_group_id` | integer | false | — | — | false | — | — | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | decimal | false | — | — | false | — | — | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | decimal | true | — | — | false | — | — | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | decimal | true | — | — | false | — | — | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the trailing rule is active. |
| `description` | string | true | — | — | false | — | — | Describes the trailing rule. |

- **Primary Key:** `id`
- **Relations:** `trailing_group_id` → Trailing Group.`id`
- **Uniqueness Constraints:** (`name`); (`trailing_group_id`, `trigger_percentage`)
- **Indexes:** none

### Partial Group

Exported as `PartialGroup`.

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `user_id` | integer | false | — | — | false | — | — | Identifies the user who owns the partial group. |
| `name` | string | false | — | — | false | — | — | The partial group's display name. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the partial group is active. |
| `description` | string | true | — | — | false | — | — | Describes the partial group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Partial Rule

Exported as `PartialRule`.

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `name` | string | false | — | — | false | — | — | The partial rule's display name. |
| `partial_group_id` | integer | false | — | — | false | — | — | Identifies the partial group that contains the rule. |
| `profit_percentage` | decimal | false | — | — | false | — | — | Defines the profit percentage that activates the rule. |
| `close_percentage` | decimal | false | — | — | false | — | — | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the partial rule is active. |
| `description` | string | true | — | — | false | — | — | Describes the partial rule. |

- **Primary Key:** `id`
- **Relations:** `partial_group_id` → Partial Group.`id`
- **Uniqueness Constraints:** (`name`); (`partial_group_id`, `profit_percentage`)
- **Indexes:** none

### Action Group

Exported as `ActionGroup`.

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `user_id` | integer | false | — | — | false | — | — | Identifies the user who owns the action group. |
| `name` | string | false | — | — | false | — | — | The action group's display name. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the action group is active. |
| `description` | string | true | — | — | false | — | — | Describes the action group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Action

Exported as `Action`.

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `name` | string | false | — | — | false | — | — | The action's display name. |
| `action_group_id` | integer | false | — | — | false | — | — | Identifies the action group that contains the action. |
| `asset_id` | integer | false | — | — | false | — | — | Identifies the asset traded by the action. |
| `account_id` | integer | false | — | — | false | — | — | Identifies the account used to execute the action. |
| `partial_group_id` | integer | false | — | — | false | — | — | Identifies the Partial Group used by the action. |
| `trailing_group_id` | integer | false | — | — | false | — | — | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | decimal | false | — | — | false | — | — | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | decimal | false | — | — | false | — | — | Defines the Take Profit value used by the action. |
| `stop_loss` | decimal | false | — | — | false | — | — | Defines the Stop Loss value used by the action. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the action is active. |
| `description` | string | true | — | — | false | — | — | Describes the action. |

- **Primary Key:** `id`
- **Relations:** `action_group_id` → Action Group.`id`; `asset_id` → Asset.`id`; `account_id` → Account.`id`; `partial_group_id` → Partial Group.`id`; `trailing_group_id` → Trailing Group.`id`
- **Uniqueness Constraints:** (`action_group_id`, `name`)
- **Indexes:** none

### Position

Exported as `Position`.

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | false | — | — | true | — | auto_increment | — |
| `user_id` | integer | false | — | — | false | — | — | Identifies the user who owns the position. |
| `name` | string | false | — | — | false | — | — | The position's display name. |
| `trading_platform_id` | integer | false | — | — | false | — | — | Identifies the trading platform used to execute the position. |
| `broker_id` | integer | false | — | — | false | — | — | Identifies the broker through which the position is executed. |
| `account_id` | integer | false | — | — | false | — | — | Identifies the trading account used for the position. |
| `trailing_group_id` | integer | false | — | — | false | — | — | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | integer | false | — | — | false | — | — | Identifies the Partial Group applied to the position. |
| `action_group_id` | integer | false | — | — | false | — | — | Identifies the Action Group associated with the position. |
| `action_id` | integer | false | — | — | false | — | — | Identifies the action from which the position is created. |
| `date` | datetime | false | — | — | false | — | — | Stores the position's date and time. |
| `volume` | decimal | false | — | — | false | — | — | Stores the position's trading volume. |
| `profit` | decimal | false | Decimal('0') | — | false | — | — | Stores the position's current profit or loss. |
| `is_executed` | boolean | false | false | — | false | — | — | Indicates whether the position has been executed. |
| `order_type` | string | false | — | — | false | — | — | Stores the position's order type. |
| `base_tp` | decimal | false | — | — | false | — | — | Stores the position's initial Take Profit value. |
| `base_sl` | decimal | false | — | — | false | — | — | Stores the position's initial Stop Loss value. |
| `real_tp` | decimal | false | — | — | false | — | — | Stores the position's current Take Profit value. |
| `real_sl` | decimal | false | — | — | false | — | — | Stores the position's current Stop Loss value. |
| `is_active` | boolean | false | true | — | false | — | — | Indicates whether the position is active. |
| `description` | string | true | — | — | false | — | — | Describes the position. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`; `trading_platform_id` → Trading Platform.`id`; `broker_id` → Broker.`id`; `account_id` → Account.`id`; `trailing_group_id` → Trailing Group.`id`; `partial_group_id` → Partial Group.`id`; `action_group_id` → Action Group.`id`; `action_id` → Action.`id`
- **Uniqueness Constraints:** (`name`)
- **Indexes:** none

## Declaration

Every Entity exposes its complete public Declaration as the class attribute `declaration`. The Declaration is an immutable record: it cannot be changed, and an Entity type cannot be given a different one.

```python
from model import Instance

declaration = Instance.declaration

print(declaration.name, "-", declaration.description)
print([field.name for field in declaration.fields])  # Fields, in Declaration order
print(declaration.primary_key)
print(declaration.relations)  # local_field, target_entity, target_field
print(declaration.unique_constraints)  # each holds an ordered tuple of Field names
print(declaration.indexes)

field = declaration.fields[3]
print(field.name, field.type, field.nullable, field.description)
print(
    field.default,
    field.sensitivity,
    field.immutable,
    field.constraints,
    field.value_generation,
)
```

A Field Declaration distinguishes a Field that has no Default Value from a Field whose Default Value is null. A Field without a Default Value holds the `ABSENT` marker, published by the Declaration contract:

```python
from model import Currency
from model.core.declaration import ABSENT

code = Currency.declaration.fields[2]
digits = Currency.declaration.fields[5]

print(code.name, code.default is ABSENT)  # True: no Default Value
print(digits.name, digits.default)  # 2
```

## Foundation

Every Entity extends Foundation, which converts it to and from JSON text.

`to_json` returns JSON text with one root object whose keys are exactly the Field names, in Declaration order. A decimal becomes its exact text, a datetime becomes an ISO 8601 string with its offset, and a pending Auto Increment value becomes null.

```python
from model import Broker

print(Broker(name="Example Broker", user_id=1).to_json())
```

`from_json` rejects malformed text, a repeated key, a non-standard constant and a root that is not one object. It decodes decimal, datetime, date, time and uuid values by each Field's Type and then builds the Entity under the same rules as direct construction. JSON null for an Auto Increment Field means the value is still pending.

```python
from model import Broker

broker = Broker.from_json(
    '{"id": null, "name": "Example Broker", "user_id": 1, "is_active": true, "description": null}'
)
print(broker.name)
```

A complete round trip, from Entity to JSON text and back, loses nothing:

```python
from decimal import Decimal

from model import TrailingRule

rule = TrailingRule(
    name="Example rule", trailing_group_id=1, trigger_percentage=Decimal("50.125")
)
text = rule.to_json()
copy = TrailingRule.from_json(text)

print(text)
print(copy.trigger_percentage == rule.trigger_percentage, copy.to_json() == text)
```

## Setup

Model is a Python library managed with [uv](https://docs.astral.sh/uv/). It needs Python 3.14 or newer.

1. Install the dependencies and build the package from the Component directory:

   ```bash
   uv sync
   ```

2. To use Model from another Component in the same repository, declare it as a local path dependency in that Component's `pyproject.toml`, then run `uv sync` there:

   ```toml
   [project]
   dependencies = ["model"]

   [tool.uv.sources]
   model = { path = "../model" }
   ```

3. Confirm the installation:

   ```bash
   uv run python -c "import model; print(len(model.entities))"
   ```

   It prints `15`.

## Use

Work with one Entity through its own export. Values are validated strictly: nothing is coerced, undeclared Fields are refused, and a Required Field must be supplied.

```python
from model import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(currency.decimal_digits)  # 2, the declared Default Value

currency.symbol = "US$"  # a mutable Field validates the whole Entity first
print(currency.symbol)
```

An immutable Field and an Auto Increment Field cannot be assigned or supplied, and a failed assignment keeps the previous value:

```python
from model import Currency

currency = Currency(user_id=1, code="USD")

try:
    currency.id = 5
except ValueError as error:
    print(error)

try:
    currency.code = "TOOLONG"
except ValueError:
    print(currency.code)  # USD, unchanged
```

Work with all Entities through the Entity Collection:

```python
from model import entities

for entity in entities:
    print(entity.declaration.name, len(entity.declaration.fields))
```

The table-ready form of every Entity is registered in one shared table metadata, reached through the Entities themselves. It holds exactly the Model tables and no others:

```python
from model import User

print(sorted(User.metadata.tables))
```

## Verify

Run the following in the Component environment (`uv run python`). It checks the shape of the published Interface, exact export membership, the Entity Collection's membership, order and correspondence with the exports, that every item is the actual Entity exposing its own actual Declaration, immutability, side-effect freedom, representative construction, Declaration access and a lossless JSON text round trip.

```python
import dataclasses
import importlib
import threading
from decimal import Decimal

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

threads_before = threading.active_count()
model = importlib.import_module("model")
assert threading.active_count() == threads_before  # loading starts nothing

# Shape: exactly the exports and the collection are published.
assert sorted(model.__all__) == sorted([*expected, "entities"])

# Exports and collection: one export per Entity, collection in Target order, same actual objects.
assert isinstance(model.entities, tuple) and len(model.entities) == len(expected)
for name, entity in zip(expected, model.entities, strict=True):
    assert getattr(model, name) is entity and entity.__name__ == name
    declaration = entity.declaration  # the Entity's own actual Declaration
    assert dataclasses.is_dataclass(declaration)

# Immutability: a Declaration and the collection cannot be changed.
try:
    model.User.declaration.name = "Other"
except dataclasses.FrozenInstanceError:
    pass
else:
    raise AssertionError("a Declaration changed")
assert not hasattr(model.entities, "append")

# Representative construction and Declaration access.
rule = model.TrailingRule(
    name="Check rule", trailing_group_id=1, trigger_percentage=Decimal("10.5")
)
assert [field.name for field in rule.declaration.fields][0] == "id" and rule.id is None
for bad in ({"name": 5}, {"unknown": 1}, {}):
    try:
        model.User(**bad)
    except ValueError:
        pass
    else:
        raise AssertionError("an invalid construction was accepted")

# Lossless JSON text round trip.
assert model.TrailingRule.from_json(rule.to_json()).to_json() == rule.to_json()
print("Model verified")
```

## Troubleshooting

| Symptom | Cause | Remedy |
|---|---|---|
| `ValueError` naming an Auto Increment Field such as `id` when constructing or assigning | The value is assigned by storage and cannot be supplied. | Omit the Field; it stays pending (`None`) until storage assigns it. |
| `from_json` raises for text that carries a non-null `id` | JSON reconstruction follows direct construction, which refuses a supplied Auto Increment value. | Remove the `id` key or set it to `null`. |
| `ValidationError` for a value that looks right | Validation is strict and never coerces: `"1"` is not an integer, `1` is not a float, a float is not a decimal, and a bool is not an integer. | Pass the exact Type: `Decimal("1.5")` for decimals, `1.0` for floats, timezone-aware values for datetimes. |
| `ValidationError` for a datetime | A datetime must be timezone-aware. | Attach a timezone, for example `datetime(2024, 1, 2, tzinfo=timezone.utc)`. |
| `ValidationError` mentions an extra input | The Field is not declared by the Entity. | Check the Field name against the Entity's Declaration. |
| `ValueError` saying a Field is immutable | `id` and any other immutable Field cannot change after construction. | Create a new Entity instead. |
| `TypeError: unhashable type` | A mutable Entity is not hashable. | Key collections by a Field value, not by the Entity. |
| `DefinitionError` when importing Model | An Entity type disagrees with its Declaration (type name, table name, or the Fields and their order). | Regenerate or correct the Entity so it matches its Declaration exactly. |
| `DeclarationError` when importing Model | A Declaration breaks a structural rule, for example a Default Value together with Value Generation. | Correct the Declaration; the message names the Entity or Field. |
| A table is missing or an unrelated table appears when creating tables | Tables were created from a different metadata. | Create tables from the Entities' own shared metadata, for example `User.metadata`. |
| Validation messages show `[redacted]` instead of a value | The Field carries a Sensitivity Marker, so its input is withheld from messages. | Check the value against the Field's Declaration. |

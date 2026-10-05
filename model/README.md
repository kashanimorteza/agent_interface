# Model

## Overview

Model is the application's reusable data library. It defines every data concept of the Trading Assistant once, as a flat **Entity** with a complete public **Declaration** and a lossless JSON conversion, and publishes all of them through one entry point. It stores nothing, runs no queries and holds no application behaviour.

```python
from model.interface import TradingPlatform

platform = TradingPlatform(name="Example Platform", code="example")
print(platform.to_json())
# {"id": null, "name": "Example Platform", "code": "example", "is_active": true, "description": null}
```

## Interface

Everything Model publishes comes from one entry point, `model.interface`:

- **Entity Exports** — every Entity is importable by its own name.
- **Entity Collection** — `entities`, an immutable tuple of every Entity class in Target order. It holds exactly the exported Entities, each once.

Nothing else is published, and loading the entry point has no side effect.

A consumer working with one Entity imports it by name:

```python
from model.interface import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States", decimal_digits=2)
```

A consumer working with all Entities enumerates the collection:

```python
from model.interface import entities

for entity in entities:
    print(entity.declaration.name)
```

### Entities

The 15 Entities, in Target order. Every Entity also carries an immutable `id` (auto increment, left `None` until storage assigns it) and a mutable boolean `is_active`. A field marked `—` under Default has no default value; a nullable field without one is `null` when omitted.

#### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `name` | `string` | no | — | — | The user's display name. |
| `username` | `string` | no | — | — | The username used to identify the user. |
| `password` | `string` | no | — | — | The password credential used by the user. |
| `api_key` | `string` | no | — | — | The API key assigned to the user. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the user is active. |
| `description` | `string` | yes | — | — | Describes the user. |

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** `name`; `username`
- **Indexes:** none

#### Trading Platform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `name` | `string` | no | — | — | The platform's display name. |
| `code` | `string` | no | — | — | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the platform is active. |
| `description` | `string` | yes | — | — | Describes the platform. |

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** `name`
- **Indexes:** none

#### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `user_id` | `integer` | no | — | — | Identifies the user who owns this instance. |
| `trading_platform_id` | `integer` | no | — | — | Identifies the trading platform used by this instance. |
| `name` | `string` | no | — | — | The instance's display name. |
| `ip` | `string` | yes | — | — | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | `string` | yes | — | — | Defines the technical username used to establish the Instance connection when required. |
| `password` | `string` | yes | — | — | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | `string` | yes | — | — | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the instance is active. |
| `description` | `string` | yes | — | — | Describes the instance. |

- **Primary Key:** `id`
- **Relations:** `user_id` → `User.id`; `trading_platform_id` → `Trading Platform.id`
- **Uniqueness Constraints:** `user_id, name`
- **Indexes:** none

#### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `user_id` | `integer` | no | — | — | Identifies the user who owns this currency. |
| `code` | `string` | no | — | size 3 | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | `string` | yes | — | — | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | `string` | yes | — | — | Identifies the country or region associated with the currency. |
| `decimal_digits` | `integer` | no | `2` | — | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the currency is active. |
| `description` | `string` | yes | — | — | Describes the currency. |

- **Primary Key:** `id`
- **Relations:** `user_id` → `User.id`
- **Uniqueness Constraints:** `user_id, code`
- **Indexes:** none

#### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `name` | `string` | no | — | — | The broker's display name. |
| `user_id` | `integer` | no | — | — | Identifies the user who owns the broker configuration. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the broker is active. |
| `description` | `string` | yes | — | — | Describes the broker. |

- **Primary Key:** `id`
- **Relations:** `user_id` → `User.id`
- **Uniqueness Constraints:** `user_id, name`
- **Indexes:** none

#### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `broker_id` | `integer` | no | — | — | Identifies the broker that provides this asset. |
| `symbol` | `string` | no | — | — | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | `string` | no | — | — | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | `float` | no | `0.0` | — | Stores the size of one point for the asset. |
| `digits` | `integer` | no | `0` | — | Stores the number of decimal digits used for the asset's price. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the asset is active. |
| `description` | `string` | yes | — | — | Describes the asset. |

- **Primary Key:** `id`
- **Relations:** `broker_id` → `Broker.id`
- **Uniqueness Constraints:** `broker_id, symbol`
- **Indexes:** none

#### Account Group

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `user_id` | `integer` | no | — | — | Identifies the user who owns the account group. |
| `name` | `string` | no | — | — | The account group's display name. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the account group is active. |
| `description` | `string` | yes | — | — | Describes the account group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → `User.id`
- **Uniqueness Constraints:** `user_id, name`
- **Indexes:** none

#### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `name` | `string` | no | — | — | The account's display name. |
| `group_id` | `integer` | no | — | — | Identifies the account group that contains the account. |
| `broker_id` | `integer` | no | — | — | Identifies the broker that owns the account. |
| `instance_id` | `integer` | no | — | — | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | `integer` | no | — | — | Identifies the base currency used by the account. |
| `username` | `string` | no | — | — | The username identifier used to access the trading account. |
| `password` | `string` | no | — | — | The credential used to access the trading account. |
| `leverage` | `integer` | no | — | — | Defines the account's leverage multiplier. |
| `balance` | `decimal` | no | `0` | — | Stores the account's current balance. |
| `account_type` | `string` | no | — | — | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the account is active. |
| `description` | `string` | yes | — | — | Describes the account. |

- **Primary Key:** `id`
- **Relations:** `group_id` → `Account Group.id`; `broker_id` → `Broker.id`; `instance_id` → `Instance.id`; `base_currency_id` → `Currency.id`
- **Uniqueness Constraints:** `name`; `group_id, broker_id, instance_id`
- **Indexes:** none

#### Trailing Group

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `user_id` | `integer` | no | — | — | Identifies the user who owns the trailing group. |
| `name` | `string` | no | — | — | The trailing group's display name. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the trailing group is active. |
| `description` | `string` | yes | — | — | Describes the trailing group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → `User.id`
- **Uniqueness Constraints:** `user_id, name`
- **Indexes:** none

#### Trailing Rule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `name` | `string` | no | — | — | The trailing rule's display name. |
| `trailing_group_id` | `integer` | no | — | — | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | `decimal` | no | — | — | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | `decimal` | yes | — | — | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | `decimal` | yes | — | — | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the trailing rule is active. |
| `description` | `string` | yes | — | — | Describes the trailing rule. |

- **Primary Key:** `id`
- **Relations:** `trailing_group_id` → `Trailing Group.id`
- **Uniqueness Constraints:** `name`; `trailing_group_id, trigger_percentage`
- **Indexes:** none

#### Partial Group

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `user_id` | `integer` | no | — | — | Identifies the user who owns the partial group. |
| `name` | `string` | no | — | — | The partial group's display name. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the partial group is active. |
| `description` | `string` | yes | — | — | Describes the partial group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → `User.id`
- **Uniqueness Constraints:** `user_id, name`
- **Indexes:** none

#### Partial Rule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `name` | `string` | no | — | — | The partial rule's display name. |
| `partial_group_id` | `integer` | no | — | — | Identifies the partial group that contains the rule. |
| `profit_percentage` | `decimal` | no | — | — | Defines the profit percentage that activates the rule. |
| `close_percentage` | `decimal` | no | — | — | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the partial rule is active. |
| `description` | `string` | yes | — | — | Describes the partial rule. |

- **Primary Key:** `id`
- **Relations:** `partial_group_id` → `Partial Group.id`
- **Uniqueness Constraints:** `name`; `partial_group_id, profit_percentage`
- **Indexes:** none

#### Action Group

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `user_id` | `integer` | no | — | — | Identifies the user who owns the action group. |
| `name` | `string` | no | — | — | The action group's display name. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the action group is active. |
| `description` | `string` | yes | — | — | Describes the action group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → `User.id`
- **Uniqueness Constraints:** `user_id, name`
- **Indexes:** none

#### Action

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `name` | `string` | no | — | — | The action's display name. |
| `action_group_id` | `integer` | no | — | — | Identifies the action group that contains the action. |
| `asset_id` | `integer` | no | — | — | Identifies the asset traded by the action. |
| `account_id` | `integer` | no | — | — | Identifies the account used to execute the action. |
| `partial_group_id` | `integer` | no | — | — | Identifies the Partial Group used by the action. |
| `trailing_group_id` | `integer` | no | — | — | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | `decimal` | no | — | — | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | `decimal` | no | — | — | Defines the Take Profit value used by the action. |
| `stop_loss` | `decimal` | no | — | — | Defines the Stop Loss value used by the action. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the action is active. |
| `description` | `string` | yes | — | — | Describes the action. |

- **Primary Key:** `id`
- **Relations:** `action_group_id` → `Action Group.id`; `asset_id` → `Asset.id`; `account_id` → `Account.id`; `partial_group_id` → `Partial Group.id`; `trailing_group_id` → `Trailing Group.id`
- **Uniqueness Constraints:** `action_group_id, name`
- **Indexes:** none

#### Position

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Nullable | Default | Properties | Description |
|---|---|---|---|---|---|
| `id` | `integer` | no | — | immutable, auto increment | — |
| `user_id` | `integer` | no | — | — | Identifies the user who owns the position. |
| `name` | `string` | no | — | — | The position's display name. |
| `trading_platform_id` | `integer` | no | — | — | Identifies the trading platform used to execute the position. |
| `broker_id` | `integer` | no | — | — | Identifies the broker through which the position is executed. |
| `account_id` | `integer` | no | — | — | Identifies the trading account used for the position. |
| `trailing_group_id` | `integer` | no | — | — | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | `integer` | no | — | — | Identifies the Partial Group applied to the position. |
| `action_group_id` | `integer` | no | — | — | Identifies the Action Group associated with the position. |
| `action_id` | `integer` | no | — | — | Identifies the action from which the position is created. |
| `date` | `datetime` | no | — | — | Stores the position's date and time. |
| `volume` | `decimal` | no | — | — | Stores the position's trading volume. |
| `profit` | `decimal` | no | `0` | — | Stores the position's current profit or loss. |
| `is_executed` | `boolean` | no | `false` | — | Indicates whether the position has been executed. |
| `order_type` | `string` | no | — | — | Stores the position's order type. |
| `base_tp` | `decimal` | no | — | — | Stores the position's initial Take Profit value. |
| `base_sl` | `decimal` | no | — | — | Stores the position's initial Stop Loss value. |
| `real_tp` | `decimal` | no | — | — | Stores the position's current Take Profit value. |
| `real_sl` | `decimal` | no | — | — | Stores the position's current Stop Loss value. |
| `is_active` | `boolean` | no | `true` | — | Indicates whether the position is active. |
| `description` | `string` | yes | — | — | Describes the position. |

- **Primary Key:** `id`
- **Relations:** `user_id` → `User.id`; `trading_platform_id` → `Trading Platform.id`; `broker_id` → `Broker.id`; `account_id` → `Account.id`; `trailing_group_id` → `Trailing Group.id`; `partial_group_id` → `Partial Group.id`; `action_group_id` → `Action Group.id`; `action_id` → `Action.id`
- **Uniqueness Constraints:** `name`
- **Indexes:** none

## Declaration

Every Entity exposes its complete logical meaning as the class attribute `declaration`, read through the Entity itself:

```python
from model.interface import TradingPlatform

declaration = TradingPlatform.declaration
declaration.name                 # "Trading Platform"
[f.name for f in declaration.fields]
# ["id", "name", "code", "is_active", "description"]
declaration.primary_key          # "id"
declaration.relations            # ()
declaration.unique_constraints   # (UniqueConstraintDeclaration(fields=("name",)),)
declaration.indexes              # ()
```

An Entity Declaration has `name`, `description`, `fields`, `primary_key`, `relations`, `unique_constraints` and `indexes`. Each Field Declaration has `name`, `description`, `type`, `nullable`, `default`, `sensitivity`, `immutable`, `constraints`, `value_generation`, plus the derived `has_default` and `required`. A Relation has `local_field`, `target_entity` and `target_field`, naming the Entity and Field by their logical names. A Field without a default has `default` set to `NO_DEFAULT`, which differs from an explicit `None`.

## Foundation

Every Entity converts to and from JSON text through two methods.

`to_json()` returns one JSON object whose keys are exactly the Entity's Field names, in Declaration order. Decimal values are exact strings, datetimes are ISO 8601 text with an offset, and a pending `id` is `null`:

```python
from model.interface import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States", decimal_digits=2)
text = currency.to_json()
# {"id": null, "user_id": 1, "code": "USD", "symbol": "$", "country": "United States", "decimal_digits": 2, "is_active": true, "description": null}
```

`from_json(text)` rebuilds an Entity under the same strict rules as direct construction. It rejects malformed text, a non-object root, duplicate keys, `NaN`/`Infinity`, unknown keys and any value of the wrong type:

```python
from model.interface import Currency

text = '{"id": null, "user_id": 1, "code": "USD", "symbol": "$", "country": "United States", "decimal_digits": 2, "is_active": true, "description": null}'
restored = Currency.from_json(text)
```

A complete round trip returns an equal Entity:

```python
from model.interface import Currency

original = Currency(user_id=1, code="USD", symbol="$", country="United States", decimal_digits=2)
restored = Currency.from_json(original.to_json())
assert restored == original
```

## Setup

Model needs Python 3.14 or newer and [uv](https://docs.astral.sh/uv/). From the Component root:

```bash
uv sync --locked
```

This creates an isolated environment from the lock file and installs the runtime dependencies (SQLModel, Pydantic, SQLAlchemy) and the development tools (Ruff, Pyright).

## Use

Import an Entity by name, or enumerate the collection; both come from the entry point.

```python
from model.interface import User, entities

user = User(name="Example", username="example", password="example-password", api_key="example-key")
user.is_active = False          # mutable fields revalidate on assignment
user.to_json()                  # lossless JSON text

[entity.declaration.name for entity in entities]
```

Construction and assignment are strict: only declared fields are accepted, values must already have the declared type (no coercion), required values must be present, and an explicit `False`, `0`, empty string or `None` is kept exactly as supplied. A failed assignment leaves the previous value unchanged. `id` cannot be supplied or changed by a consumer.

Every Entity is a table model whose storage mapping is ready for a storage component to use: the table is named after the Entity with its spaces removed, columns are named after Fields, and the shared metadata is reachable through any Entity, for example `User.metadata`. Model itself never opens a connection or writes data.

## Verify

Run the following from the Component root with `uv run python`. It checks the entry-point shape, exact export membership, the collection's membership and order and its correspondence with the exports, actual Entity and Declaration references, immutability, representative construction, Declaration access and a lossless JSON round trip.

```python
from model.interface import (
    Account, AccountGroup, Action, ActionGroup, Asset, Broker, Currency, Instance,
    PartialGroup, PartialRule, Position, TradingPlatform, TrailingGroup, TrailingRule,
    User, entities,
)

# membership and order: the collection is exactly the exports, in Target order
assert entities == (
    User, TradingPlatform, Instance, Currency, Broker, Asset, AccountGroup, Account,
    TrailingGroup, TrailingRule, PartialGroup, PartialRule, ActionGroup, Action, Position,
)
assert isinstance(entities, tuple)                       # immutable

# actual references: each Entity carries its own Declaration
assert all(entity.declaration.primary_key == "id" for entity in entities)
assert [entity.declaration.name for entity in entities][:2] == ["User", "Trading Platform"]

# representative construction, immutability and a lossless round trip
platform = TradingPlatform(name="Example Platform", code="example")
assert platform.id is None and platform.is_active is True
try:
    platform.id = 1
except ValueError:
    pass
else:
    raise AssertionError("id must be immutable")
assert TradingPlatform.from_json(platform.to_json()) == platform
```

To confirm that loading has no side effect, run the import from an empty directory and check that no file, connection or process results. Run `uv run ruff check src`, `uv run ruff format --check src` and `uv run pyright src` to check source quality.

## Troubleshooting

- **`ValueError` naming a field on construction or assignment** — the value broke that Field's contract (wrong type, missing required value, size, nullability). The message names the field and the rule, never the value of a sensitive field.
- **`unknown fields [...]`** — the name is not a declared Field of that Entity; check its table in the Interface section.
- **`generated fields ['id'] cannot be supplied`** — `id` is assigned by storage; leave it out when constructing.
- **`field 'id' is immutable`** — an assigned identity cannot be changed.
- **`from_json` rejects the text** — it must be standard JSON with one object at its root, no duplicate or unknown keys, decimals as strings and datetimes as ISO 8601 text with an offset.
- **`unrecognized Type`** — a Declaration used a Type outside `string`, `integer`, `float`, `decimal`, `boolean`, `datetime`, `date`, `time`, `uuid`; no Entity is created from it.
- **Installation fails or versions differ** — run `uv sync --locked` from the Component root to reproduce the locked environment.

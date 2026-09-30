# Model

Model publishes the reusable, technology-independent data-model Entities of the Trading Assistant. Every Entity carries its own Fields, Entity Metadata, and a public Declaration that states its complete meaning. Model defines what the data means; it stores nothing, performs no operation on it, and depends on no other Component.

```python
from model import User

user = User(name="Admin", username="admin", password="change-me", api_key="change-me-too")
print(user.is_active)  # True
```

## Interface

The package exports every Entity by its own name, and one ordered, immutable collection named `entities` that holds all of them in the order below. Import the Entity you work with directly, or enumerate the collection when you work with all of them. Nothing else is published as an Entity, and importing `model` has no side effect.

Import one Entity directly:

```python
from model import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States", decimal_digits=2)
print(currency.code)  # USD
```

Enumerate every Entity:

```python
from model import entities

for entity in entities:
    print(entity.declaration.name)
```

### Entities

Every Entity has an immutable, non-nullable `id` and a mutable, non-nullable Boolean `is_active`. Logical names keep the exact spelling shown here; the exported class name is the logical name without spaces.

#### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `name` | `string` | no | none | The user's display name. | required |
| `username` | `string` | no | none | The username used to identify the user. | required |
| `password` | `string` | no | none | The password credential used by the user. | required; sensitivity marker `password` |
| `api_key` | `string` | no | none | The API key assigned to the user. | required; sensitivity marker `sensitive` |
| `is_active` | `boolean` | no | `true` | Indicates whether the user is active. | none |
| `description` | `string` | yes | none | Describes the user. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - none
- Uniqueness Constraints:
  - (`name`)
  - (`username`)
- Indexes: none

#### Trading Platform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `name` | `string` | no | none | The platform's display name. | required |
| `code` | `string` | no | none | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. | required |
| `is_active` | `boolean` | no | `true` | Indicates whether the platform is active. | none |
| `description` | `string` | yes | none | Describes the platform. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - none
- Uniqueness Constraints:
  - (`name`)
- Indexes: none

#### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `user_id` | `integer` | no | none | Identifies the user who owns this instance. | required |
| `trading_platform_id` | `integer` | no | none | Identifies the trading platform used by this instance. | required |
| `name` | `string` | no | none | The instance's display name. | required |
| `ip` | `string` | yes | none | Identifies the technical network address used to reach the Trading Platform when required. | none |
| `username` | `string` | yes | none | Defines the technical username used to establish the Instance connection when required. | none |
| `password` | `string` | yes | none | Defines the technical password used to establish the Instance connection when required. | sensitivity marker `password` |
| `api_key` | `string` | yes | none | Defines the technical API credential used to establish the Instance connection when required. | sensitivity marker `sensitive` |
| `is_active` | `boolean` | no | `true` | Indicates whether the instance is active. | none |
| `description` | `string` | yes | none | Describes the instance. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
  - `trading_platform_id` → `Trading Platform.id`
- Uniqueness Constraints:
  - (`user_id`, `name`)
- Indexes: none

#### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `user_id` | `integer` | no | none | Identifies the user who owns this currency. | required |
| `code` | `string` | no | none | The currency's standard three-letter code, such as `USD` or `EUR`. | required; size 3 |
| `symbol` | `string` | yes | none | The currency's display symbol, such as `$`, `€`, or `£`. | none |
| `country` | `string` | yes | none | Identifies the country or region associated with the currency. | none |
| `decimal_digits` | `integer` | no | `2` | Defines the number of decimal digits normally used for monetary values in the currency. | none |
| `is_active` | `boolean` | no | `true` | Indicates whether the currency is active. | none |
| `description` | `string` | yes | none | Describes the currency. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
- Uniqueness Constraints:
  - (`user_id`, `code`)
- Indexes: none

#### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `name` | `string` | no | none | The broker's display name. | required |
| `user_id` | `integer` | no | none | Identifies the user who owns the broker configuration. | required |
| `is_active` | `boolean` | no | `true` | Indicates whether the broker is active. | none |
| `description` | `string` | yes | none | Describes the broker. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
- Uniqueness Constraints:
  - (`user_id`, `name`)
- Indexes: none

#### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `broker_id` | `integer` | no | none | Identifies the broker that provides this asset. | required |
| `symbol` | `string` | no | none | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. | required |
| `category` | `string` | no | none | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. | required |
| `point_size` | `float` | no | `0.0` | Stores the size of one point for the asset. | none |
| `digits` | `integer` | no | `0` | Stores the number of decimal digits used for the asset's price. | none |
| `is_active` | `boolean` | no | `true` | Indicates whether the asset is active. | none |
| `description` | `string` | yes | none | Describes the asset. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - `broker_id` → `Broker.id`
- Uniqueness Constraints:
  - (`broker_id`, `symbol`)
- Indexes: none

#### Account Group

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `user_id` | `integer` | no | none | Identifies the user who owns the account group. | required |
| `name` | `string` | no | none | The account group's display name. | required |
| `is_active` | `boolean` | no | `true` | Indicates whether the account group is active. | none |
| `description` | `string` | yes | none | Describes the account group. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
- Uniqueness Constraints:
  - (`user_id`, `name`)
- Indexes: none

#### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `name` | `string` | no | none | The account's display name. | required |
| `group_id` | `integer` | no | none | Identifies the account group that contains the account. | required |
| `broker_id` | `integer` | no | none | Identifies the broker that owns the account. | required |
| `instance_id` | `integer` | no | none | Identifies the trading-platform instance used to connect this account. | required |
| `base_currency_id` | `integer` | no | none | Identifies the base currency used by the account. | required |
| `username` | `string` | no | none | The username identifier used to access the trading account. | required |
| `password` | `string` | no | none | The credential used to access the trading account. | required; sensitivity marker `password` |
| `leverage` | `integer` | no | none | Defines the account's leverage multiplier. | required |
| `balance` | `decimal` | no | `0` | Stores the account's current balance. | none |
| `account_type` | `string` | no | none | Identifies the account model, such as `cfd` or `spread_betting`. | required |
| `is_active` | `boolean` | no | `true` | Indicates whether the account is active. | none |
| `description` | `string` | yes | none | Describes the account. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - `group_id` → `Account Group.id`
  - `broker_id` → `Broker.id`
  - `instance_id` → `Instance.id`
  - `base_currency_id` → `Currency.id`
- Uniqueness Constraints:
  - (`name`)
  - (`group_id`, `broker_id`, `instance_id`)
- Indexes: none

#### Trailing Group

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `user_id` | `integer` | no | none | Identifies the user who owns the trailing group. | required |
| `name` | `string` | no | none | The trailing group's display name. | required |
| `is_active` | `boolean` | no | `true` | Indicates whether the trailing group is active. | none |
| `description` | `string` | yes | none | Describes the trailing group. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
- Uniqueness Constraints:
  - (`user_id`, `name`)
- Indexes: none

#### Trailing Rule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `name` | `string` | no | none | The trailing rule's display name. | required |
| `trailing_group_id` | `integer` | no | none | Identifies the trailing group that contains the rule. | required |
| `trigger_percentage` | `decimal` | no | none | Defines the profit percentage of the take-profit target that activates the rule. | required |
| `take_profit_adjustment` | `decimal` | yes | none | Defines the take-profit adjustment applied when the rule is activated. | none |
| `stop_loss_adjustment` | `decimal` | yes | none | Defines the stop-loss adjustment applied when the rule is activated. | none |
| `is_active` | `boolean` | no | `true` | Indicates whether the trailing rule is active. | none |
| `description` | `string` | yes | none | Describes the trailing rule. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - `trailing_group_id` → `Trailing Group.id`
- Uniqueness Constraints:
  - (`name`)
  - (`trailing_group_id`, `trigger_percentage`)
- Indexes: none

#### Partial Group

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `user_id` | `integer` | no | none | Identifies the user who owns the partial group. | required |
| `name` | `string` | no | none | The partial group's display name. | required |
| `is_active` | `boolean` | no | `true` | Indicates whether the partial group is active. | none |
| `description` | `string` | yes | none | Describes the partial group. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
- Uniqueness Constraints:
  - (`user_id`, `name`)
- Indexes: none

#### Partial Rule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `name` | `string` | no | none | The partial rule's display name. | required |
| `partial_group_id` | `integer` | no | none | Identifies the partial group that contains the rule. | required |
| `profit_percentage` | `decimal` | no | none | Defines the profit percentage that activates the rule. | required |
| `close_percentage` | `decimal` | no | none | Defines the percentage of the position closed when the rule is activated. | required |
| `is_active` | `boolean` | no | `true` | Indicates whether the partial rule is active. | none |
| `description` | `string` | yes | none | Describes the partial rule. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - `partial_group_id` → `Partial Group.id`
- Uniqueness Constraints:
  - (`name`)
  - (`partial_group_id`, `profit_percentage`)
- Indexes: none

#### Action Group

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `user_id` | `integer` | no | none | Identifies the user who owns the action group. | required |
| `name` | `string` | no | none | The action group's display name. | required |
| `is_active` | `boolean` | no | `true` | Indicates whether the action group is active. | none |
| `description` | `string` | yes | none | Describes the action group. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - `user_id` → `User.id`
- Uniqueness Constraints:
  - (`user_id`, `name`)
- Indexes: none

#### Action

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `name` | `string` | no | none | The action's display name. | required |
| `action_group_id` | `integer` | no | none | Identifies the action group that contains the action. | required |
| `asset_id` | `integer` | no | none | Identifies the asset traded by the action. | required |
| `account_id` | `integer` | no | none | Identifies the account used to execute the action. | required |
| `partial_group_id` | `integer` | no | none | Identifies the Partial Group used by the action. | required |
| `trailing_group_id` | `integer` | no | none | Identifies the Trailing Group used by the action. | required |
| `risk_by_reward` | `decimal` | no | none | Defines the numeric risk-to-reward value used by the action. | required |
| `take_profit` | `decimal` | no | none | Defines the Take Profit value used by the action. | required |
| `stop_loss` | `decimal` | no | none | Defines the Stop Loss value used by the action. | required |
| `is_active` | `boolean` | no | `true` | Indicates whether the action is active. | none |
| `description` | `string` | yes | none | Describes the action. | none |

Entity Metadata:

- Primary Key: `id`
- Relations:
  - `action_group_id` → `Action Group.id`
  - `asset_id` → `Asset.id`
  - `account_id` → `Account.id`
  - `partial_group_id` → `Partial Group.id`
  - `trailing_group_id` → `Trailing Group.id`
- Uniqueness Constraints:
  - (`action_group_id`, `name`)
- Indexes: none

#### Position

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Nullable | Default | Purpose | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `integer` | no | none | none | Auto Increment; pending until its owner assigns it once; immutable once assigned |
| `user_id` | `integer` | no | none | Identifies the user who owns the position. | required |
| `name` | `string` | no | none | The position's display name. | required |
| `trading_platform_id` | `integer` | no | none | Identifies the trading platform used to execute the position. | required |
| `broker_id` | `integer` | no | none | Identifies the broker through which the position is executed. | required |
| `account_id` | `integer` | no | none | Identifies the trading account used for the position. | required |
| `trailing_group_id` | `integer` | no | none | Identifies the Trailing Group applied to the position. | required |
| `partial_group_id` | `integer` | no | none | Identifies the Partial Group applied to the position. | required |
| `action_group_id` | `integer` | no | none | Identifies the Action Group associated with the position. | required |
| `action_id` | `integer` | no | none | Identifies the action from which the position is created. | required |
| `date` | `datetime` | no | none | Stores the position's date and time. | required |
| `volume` | `decimal` | no | none | Stores the position's trading volume. | required |
| `profit` | `decimal` | no | `0` | Stores the position's current profit or loss. | none |
| `is_executed` | `boolean` | no | `false` | Indicates whether the position has been executed. | none |
| `order_type` | `string` | no | none | Stores the position's order type. | required |
| `base_tp` | `decimal` | no | none | Stores the position's initial Take Profit value. | required |
| `base_sl` | `decimal` | no | none | Stores the position's initial Stop Loss value. | required |
| `real_tp` | `decimal` | no | none | Stores the position's current Take Profit value. | required |
| `real_sl` | `decimal` | no | none | Stores the position's current Stop Loss value. | required |
| `is_active` | `boolean` | no | `true` | Indicates whether the position is active. | none |
| `description` | `string` | yes | none | Describes the position. | none |

Entity Metadata:

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
  - (`name`)
- Indexes: none

## Declaration

Every Entity exposes its complete public meaning through its `declaration` attribute. An Entity Declaration has `name`, `description`, ordered `fields`, `primary_key`, `relations`, `unique_constraints`, and `indexes`. A Field Declaration has `name`, `description`, `type`, `nullable`, `has_default` with `default`, `sensitivity`, `immutable`, `constraints`, and `value_generation`. A Relation has `local_field`, `target_entity`, and `target_field`. A Declaration is read-only and performs no behaviour.

```python
from model import Currency

declaration = Currency.declaration
print(declaration.name, declaration.primary_key)
for field in declaration.fields:
    print(field.name, field.type, field.nullable, field.has_default, field.default)
print(declaration.relations)
print(declaration.unique_constraints)
print(declaration.indexes)
```

`has_default` separates a field with no declared default from a field whose declared default is null.

## Foundation

Every Entity converts to and from JSON text. `to_json` returns text with one object at its root whose keys are exactly the Entity's Fields in Declaration order. `from_json` rebuilds an Entity from such text and rejects malformed text. Decimal values are JSON strings so their digits stay exact; datetime values are ISO 8601 strings with an offset and are held in UTC; a pending `id` is `null`.

```python
from model import Currency

currency = Currency(user_id=1, code="EUR")
text = currency.to_json()
print(text)
same = Currency.from_json(text)
print(same.code)  # EUR
```

A complete round trip with exact decimal and datetime values:

```python
from datetime import UTC, datetime
from decimal import Decimal

from model import Position

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
    date=datetime(2026, 1, 15, 9, 30, tzinfo=UTC),
    volume=Decimal("0.10"),
    order_type="buy",
    base_tp=Decimal("1.2000"),
    base_sl=Decimal("1.1000"),
    real_tp=Decimal("1.2000"),
    real_sl=Decimal("1.1000"),
)
text = position.to_json()
restored = Position.from_json(text)
assert restored.to_json() == text
assert restored.volume == Decimal("0.10") and restored.date == position.date
```

## Setup

Model needs `uv`. The dependencies and the Python version are declared in `pyproject.toml` and pinned in `uv.lock`.

1. From the Component root, create the environment: `uv sync`.
2. Check the import: `uv run python -c "import model"`.
3. To use Model from another project, add it as a dependency by path: `uv add ../model`, adjusting the path to where Model is located.

## Use

Follow the exports and the collection: import an Entity by name, or enumerate `entities`.

```python
from model import Account, User, entities

user = User(name="Admin", username="admin", password="change-me", api_key="change-me-too")
assert user.id is None  # pending: an Auto Increment Field is assigned by its owner, never supplied
user.id = 1  # the owner assigns it once
user.is_active = False  # a mutable Field revalidates on assignment
account = Account(
    name="Acc-1",
    group_id=1,
    broker_id=1,
    instance_id=1,
    base_currency_id=1,
    username="test",
    password="change-me",
    leverage=100,
    account_type="CFD",
)
print(account.balance)  # 0
print(len(entities))
```

Rules that apply to every Entity:

- Construction, `from_json`, and assignment enforce the same rules: only declared Fields, no implicit coercion, required values present, nullability and constraints respected. A failed assignment keeps the earlier value.
- An Auto Increment Field cannot be supplied on construction or in JSON; it stays pending (`None`, JSON `null`) until its owner assigns it once, and then it cannot change.
- Datetime values must be timezone-aware and are held in UTC.
- A Sensitivity Marker records meaning only. Model keeps the value unchanged, never protects, hashes, or encrypts it, and never places a sensitive value in an error message. Credential Fields named `password` carry the marker `password`; the other credential Fields carry `sensitive`.

## Verify

Run this from an environment where Model is installed. It checks the Interface shape, export membership, collection membership and order, actual references, immutability, representative construction, Declaration access, and a lossless JSON round trip.

```python
import model
from model import User, entities

expected = ["User", "TradingPlatform", "Instance", "Currency", "Broker", "Asset", "AccountGroup", "Account", "TrailingGroup", "TrailingRule", "PartialGroup", "PartialRule", "ActionGroup", "Action", "Position"]

assert [entity.__name__ for entity in entities] == expected
assert isinstance(entities, tuple)
assert all(getattr(model, name) is entity for name, entity in zip(expected, entities))
assert {n for n in vars(model.interface) if not n.startswith("_")} == set(expected) | {"entities"}
assert all("declaration" in vars(entity) for entity in entities)
assert all(entity.declaration.fields[0].name == "id" and entity.declaration.fields[0].immutable for entity in entities)
try:
    entities[0] = None
except TypeError:
    pass
else:
    raise SystemExit("the collection must be immutable")

user = User(name="Admin", username="admin", password="change-me", api_key="change-me-too")
assert user.declaration.name == "User" and user.id is None
assert User.from_json(user.to_json()).to_json() == user.to_json()
print("Model verified")
```

Importing `model` has no side effect. To confirm it, run `python -c "import model"` from an empty directory and check that the directory is still empty and no process or network activity occurred.

## Troubleshooting

- **A `ValidationError` says a Field is not allowed or has the wrong type.** Model never coerces values and rejects undeclared Fields. Pass exactly the declared Fields with values of their declared Types; an integer is not accepted for a boolean, a string is not accepted for an integer, and a decimal must be a `Decimal`.
- **A supplied `id` is rejected.** An Auto Increment Field is assigned by its owner and cannot be supplied on construction or in JSON. Construct without it, and assign it once afterwards.
- **`from_json` rejects an Entity whose `id` is already assigned.** The pending `id` (`null`) round-trips; a supplied `id` follows the same rule as construction and is rejected.
- **`from_json` rejects a decimal or datetime.** A decimal must be a JSON string such as `"1.10"` and a datetime must be an ISO 8601 string with an offset; a datetime without an offset is naive and is rejected.
- **Assigning `id` again fails.** `id` is immutable once assigned.
- **A `Currency` code is rejected.** Its code must be exactly three characters.
- **An error message does not show the offending value.** This is intended: Model never echoes a value in a diagnostic because it might be sensitive.

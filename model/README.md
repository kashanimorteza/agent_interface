# Model

## Overview

The Model is the reusable data library of the application. It defines each Target model as a flat Entity with a complete public Declaration of its meaning and a lossless JSON conversion. It stores nothing, runs no queries, and applies no encryption, hashing, or masking: it publishes what the data means.

```python
from model import Currency

usd = Currency(
    user_id=1, code="USD", symbol="$", country="United States", decimal_digits=2
)
print(usd.to_json())
```

## Interface

The Model publishes every Entity by its own name and one ordered `entities` collection. Nothing else is published: there is no registry, lookup, or wildcard export. Importing the package has no side effect: it opens no connection or file and creates no instance.

Import one Entity directly:

```python
from model import Currency
```

Enumerate every Entity in Target order:

```python
from model import entities

for entity in entities:
    print(entity.declaration.name)
```

Entities, in Target order:

### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `name` | string | no | — | — | — | no | The user's display name. |
| `username` | string | no | — | — | — | no | The username used to identify the user. |
| `password` | string | no | — | — | — | no | The password credential used by the user. |
| `api_key` | string | no | — | — | — | no | The API key assigned to the user. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the user is active. |
| `description` | string | yes | — | — | — | no | Describes the user. |

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** (`name`), (`username`)
- **Indexes:** none

### Trading Platform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `name` | string | no | — | — | — | no | The platform's display name. |
| `code` | string | no | — | — | — | no | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the platform is active. |
| `description` | string | yes | — | — | — | no | Describes the platform. |

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** (`name`)
- **Indexes:** none

### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `user_id` | integer | no | — | — | — | no | Identifies the user who owns this instance. |
| `trading_platform_id` | integer | no | — | — | — | no | Identifies the trading platform used by this instance. |
| `name` | string | no | — | — | — | no | The instance's display name. |
| `ip` | string | yes | — | — | — | no | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | string | yes | — | — | — | no | Defines the technical username used to establish the Instance connection when required. |
| `password` | string | yes | — | — | — | no | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | string | yes | — | — | — | no | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the instance is active. |
| `description` | string | yes | — | — | — | no | Describes the instance. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`, `trading_platform_id` → Trading Platform.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `user_id` | integer | no | — | — | — | no | Identifies the user who owns this currency. |
| `code` | string | no | — | size=3 | — | no | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | string | yes | — | — | — | no | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | string | yes | — | — | — | no | Identifies the country or region associated with the currency. |
| `decimal_digits` | integer | no | `2` | — | — | no | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the currency is active. |
| `description` | string | yes | — | — | — | no | Describes the currency. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `code`)
- **Indexes:** none

### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `name` | string | no | — | — | — | no | The broker's display name. |
| `user_id` | integer | no | — | — | — | no | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the broker is active. |
| `description` | string | yes | — | — | — | no | Describes the broker. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `broker_id` | integer | no | — | — | — | no | Identifies the broker that provides this asset. |
| `symbol` | string | no | — | — | — | no | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | string | no | — | — | — | no | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | float | no | `0.0` | — | — | no | Stores the size of one point for the asset. |
| `digits` | integer | no | `0` | — | — | no | Stores the number of decimal digits used for the asset's price. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the asset is active. |
| `description` | string | yes | — | — | — | no | Describes the asset. |

- **Primary Key:** `id`
- **Relations:** `broker_id` → Broker.`id`
- **Uniqueness Constraints:** (`broker_id`, `symbol`)
- **Indexes:** none

### Account Group

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `user_id` | integer | no | — | — | — | no | Identifies the user who owns the account group. |
| `name` | string | no | — | — | — | no | The account group's display name. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the account group is active. |
| `description` | string | yes | — | — | — | no | Describes the account group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `name` | string | no | — | — | — | no | The account's display name. |
| `group_id` | integer | no | — | — | — | no | Identifies the account group that contains the account. |
| `broker_id` | integer | no | — | — | — | no | Identifies the broker that owns the account. |
| `instance_id` | integer | no | — | — | — | no | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | no | — | — | — | no | Identifies the base currency used by the account. |
| `username` | string | no | — | — | — | no | The username identifier used to access the trading account. |
| `password` | string | no | — | — | — | no | The credential used to access the trading account. |
| `leverage` | integer | no | — | — | — | no | Defines the account's leverage multiplier. |
| `balance` | decimal | no | `Decimal('0')` | — | — | no | Stores the account's current balance. |
| `account_type` | string | no | — | — | — | no | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the account is active. |
| `description` | string | yes | — | — | — | no | Describes the account. |

- **Primary Key:** `id`
- **Relations:** `group_id` → Account Group.`id`, `broker_id` → Broker.`id`, `instance_id` → Instance.`id`, `base_currency_id` → Currency.`id`
- **Uniqueness Constraints:** (`name`), (`group_id`, `broker_id`, `instance_id`)
- **Indexes:** none

### Trailing Group

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `user_id` | integer | no | — | — | — | no | Identifies the user who owns the trailing group. |
| `name` | string | no | — | — | — | no | The trailing group's display name. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the trailing group is active. |
| `description` | string | yes | — | — | — | no | Describes the trailing group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Trailing Rule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `name` | string | no | — | — | — | no | The trailing rule's display name. |
| `trailing_group_id` | integer | no | — | — | — | no | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | decimal | no | — | — | — | no | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | decimal | yes | — | — | — | no | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | decimal | yes | — | — | — | no | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the trailing rule is active. |
| `description` | string | yes | — | — | — | no | Describes the trailing rule. |

- **Primary Key:** `id`
- **Relations:** `trailing_group_id` → Trailing Group.`id`
- **Uniqueness Constraints:** (`name`), (`trailing_group_id`, `trigger_percentage`)
- **Indexes:** none

### Partial Group

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `user_id` | integer | no | — | — | — | no | Identifies the user who owns the partial group. |
| `name` | string | no | — | — | — | no | The partial group's display name. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the partial group is active. |
| `description` | string | yes | — | — | — | no | Describes the partial group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Partial Rule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `name` | string | no | — | — | — | no | The partial rule's display name. |
| `partial_group_id` | integer | no | — | — | — | no | Identifies the partial group that contains the rule. |
| `profit_percentage` | decimal | no | — | — | — | no | Defines the profit percentage that activates the rule. |
| `close_percentage` | decimal | no | — | — | — | no | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the partial rule is active. |
| `description` | string | yes | — | — | — | no | Describes the partial rule. |

- **Primary Key:** `id`
- **Relations:** `partial_group_id` → Partial Group.`id`
- **Uniqueness Constraints:** (`name`), (`partial_group_id`, `profit_percentage`)
- **Indexes:** none

### Action Group

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `user_id` | integer | no | — | — | — | no | Identifies the user who owns the action group. |
| `name` | string | no | — | — | — | no | The action group's display name. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the action group is active. |
| `description` | string | yes | — | — | — | no | Describes the action group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Action

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `name` | string | no | — | — | — | no | The action's display name. |
| `action_group_id` | integer | no | — | — | — | no | Identifies the action group that contains the action. |
| `asset_id` | integer | no | — | — | — | no | Identifies the asset traded by the action. |
| `account_id` | integer | no | — | — | — | no | Identifies the account used to execute the action. |
| `partial_group_id` | integer | no | — | — | — | no | Identifies the Partial Group used by the action. |
| `trailing_group_id` | integer | no | — | — | — | no | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | decimal | no | — | — | — | no | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | decimal | no | — | — | — | no | Defines the Take Profit value used by the action. |
| `stop_loss` | decimal | no | — | — | — | no | Defines the Stop Loss value used by the action. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the action is active. |
| `description` | string | yes | — | — | — | no | Describes the action. |

- **Primary Key:** `id`
- **Relations:** `action_group_id` → Action Group.`id`, `asset_id` → Asset.`id`, `account_id` → Account.`id`, `partial_group_id` → Partial Group.`id`, `trailing_group_id` → Trailing Group.`id`
- **Uniqueness Constraints:** (`action_group_id`, `name`)
- **Indexes:** none

### Position

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Nullable | Default | Constraints | Generation | Immutable | Description |
|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | auto_increment | yes | — |
| `user_id` | integer | no | — | — | — | no | Identifies the user who owns the position. |
| `name` | string | no | — | — | — | no | The position's display name. |
| `trading_platform_id` | integer | no | — | — | — | no | Identifies the trading platform used to execute the position. |
| `broker_id` | integer | no | — | — | — | no | Identifies the broker through which the position is executed. |
| `account_id` | integer | no | — | — | — | no | Identifies the trading account used for the position. |
| `trailing_group_id` | integer | no | — | — | — | no | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | integer | no | — | — | — | no | Identifies the Partial Group applied to the position. |
| `action_group_id` | integer | no | — | — | — | no | Identifies the Action Group associated with the position. |
| `action_id` | integer | no | — | — | — | no | Identifies the action from which the position is created. |
| `date` | datetime | no | — | — | — | no | Stores the position's date and time. |
| `volume` | decimal | no | — | — | — | no | Stores the position's trading volume. |
| `profit` | decimal | no | `Decimal('0')` | — | — | no | Stores the position's current profit or loss. |
| `is_executed` | boolean | no | `False` | — | — | no | Indicates whether the position has been executed. |
| `order_type` | string | no | — | — | — | no | Stores the position's order type. |
| `base_tp` | decimal | no | — | — | — | no | Stores the position's initial Take Profit value. |
| `base_sl` | decimal | no | — | — | — | no | Stores the position's initial Stop Loss value. |
| `real_tp` | decimal | no | — | — | — | no | Stores the position's current Take Profit value. |
| `real_sl` | decimal | no | — | — | — | no | Stores the position's current Stop Loss value. |
| `is_active` | boolean | no | `True` | — | — | no | Indicates whether the position is active. |
| `description` | string | yes | — | — | — | no | Describes the position. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`, `trading_platform_id` → Trading Platform.`id`, `broker_id` → Broker.`id`, `account_id` → Account.`id`, `trailing_group_id` → Trailing Group.`id`, `partial_group_id` → Partial Group.`id`, `action_group_id` → Action Group.`id`, `action_id` → Action.`id`
- **Uniqueness Constraints:** (`name`)
- **Indexes:** none
## Declaration

Every Entity exposes its complete public Declaration through the Entity itself, as the class attribute `declaration`. A consumer never needs another lookup.

```python
from model import Instance

declaration = Instance.declaration

declaration.name  # "Instance"
declaration.description  # what the Entity is
declaration.fields  # ordered Field Declarations
declaration.primary_key  # "id"
declaration.relations  # Relations by local field, target Entity, and target field
declaration.unique_constraints  # each constraint as a tuple of field names
declaration.indexes  # each Index as a tuple of field names

field = declaration.fields[1]
field.name, field.description, field.type, field.nullable
field.default, field.sensitivity, field.immutable
field.constraints, field.value_generation
```

A Field with no Default Value reports `NO_DEFAULT` (importable from `model.core.declaration`), which differs from an explicit default of `None`.

## Foundation

Every Entity converts to and from JSON text. The root of the text is one object whose keys are exactly the Entity's Field names in Declaration order. Decimal values are exact strings, datetime values are ISO 8601 text with an offset, and `null`, `false`, zero, and the empty string stay distinct.

```python
from model import Broker

broker = Broker(name="Example Broker", user_id=1)

text = broker.to_json()  # Entity to JSON text
same = Broker.from_json(text)  # JSON text to Entity
```

A complete round trip:

```python
from model import Broker

original = Broker(name="Example Broker", user_id=1)
restored = Broker.from_json(original.to_json())
assert restored == original
```

An identity that storage has not yet assigned is `None` and appears as `null`.

## Setup

The Model is a Python library managed with `uv`.

1. Install `uv`, then from the Model's root directory create the environment from the lockfile:

   ```bash
   uv sync --locked
   ```

2. Confirm the package loads:

   ```bash
   uv run python -c "import model; print(len(model.entities))"
   ```

The development environment also provides `ruff` (formatter and linter) and `pyright` (type checker):

```bash
uv run ruff format --check .
uv run ruff check .
uv run pyright
```

## Use

Use only the published exports and the `entities` collection.

```python
from model import Currency, entities

# Direct import: construction enforces every Field contract.
currency = Currency(user_id=1, code="USD", symbol="$", country="United States")

# Mutation revalidates; a failed assignment keeps the previous value.
currency.symbol = "US$"

# Enumerating every Entity without knowing their names.
names = [entity.declaration.name for entity in entities]
```

- Omit `id`: it stays `None` until storage assigns it, and it is immutable afterwards. Supplying one on construction is rejected.
- Values are never coerced: a string where an integer is declared, an integer for a Boolean, or a float for a decimal is rejected.
- Datetime values must carry a timezone and are stored in UTC.

## Verify

This script verifies the published shape, the Entity Collection, immutability, side-effect freedom, construction, Declaration access, and a lossless JSON round trip. It prints `ok` when every check holds.

```python
import os
import tempfile

# Loading the package must not create a file, even when the working directory is empty.
with tempfile.TemporaryDirectory() as empty:
    os.chdir(empty)
    import model

    assert os.listdir(empty) == []

names = [
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
public = {n for n in dir(model) if not n.startswith("_")} - {
    "core",
    "entity",
    "interface",
}

# Exact Entity Export membership, and the collection matches the exports in Target order.
assert public == set(names) | {"entities"}
assert [e.__name__ for e in model.entities] == names
assert all(model.entities[i] is getattr(model, n) for i, n in enumerate(names))

# The collection is immutable.
assert isinstance(model.entities, tuple)

# Each Entity exposes its own actual Declaration, identically on every access.
assert all(e.declaration is e.declaration for e in model.entities)

# Representative construction, strictness, immutability, and a lossless round trip.
broker = model.Broker(name="Example Broker", user_id=1)
assert broker.id is None and broker.is_active is True
for bad in (
    {"name": 1, "user_id": 1},
    {"user_id": 1},
    {"name": "x", "user_id": 1, "unknown": 1},
):
    try:
        model.Broker(**bad)
        raise SystemExit("an invalid construction was accepted")
    except ValueError:
        pass
try:
    broker.id = 5
    raise SystemExit("an immutable Field changed")
except ValueError:
    pass
assert model.Broker.from_json(broker.to_json()) == broker
print("ok")
```

## Troubleshooting

- **`Unknown Field '<name>'`** — construction accepts only declared Fields. Check the name against the Entity's Declaration.
- **A validation error on a value of the wrong type** — values are never coerced. Pass the declared type: a decimal as `decimal.Decimal`, a datetime as a timezone-aware `datetime`.
- **`Field 'id' is generated and cannot be supplied`** — leave `id` out; storage assigns it. Reconstruction from JSON text accepts an assigned identity because that text represents a stored Entity.
- **`Field '<name>' is immutable`** — `id` cannot be assigned after construction.
- **`Field '<name>' must be a JSON string`** — in JSON text, decimals and datetimes are strings.
- **`Entity '<name>' does not realize its Declaration`** — an Entity's Fields differ from its own Declaration. Fix the Entity so both agree; the Declaration is the source of truth for primary key, unique, index, and Relation metadata.
- **Importing the package fails on a Relation** — a Relation names a target Entity or Field that does not exist in the Model, or their types differ.
- **Validation errors omit values** — this is intended: values are never echoed in diagnostics.


# Model

Model is the reusable data library of the Trading Assistant. It defines the application's data concepts once, as flat Entities, and publishes them through one package-root entrypoint.

## Overview

Every Entity is the authoritative definition of one concept of the Target. It carries its own Fields, its Entity Metadata (Primary Key, Relations, Uniqueness Constraints, Indexes), and a public Declaration that states all of it. Every Entity has an `id` Identity and an `is_active` Activity Field. Entities validate every value they receive, convert losslessly to and from JSON text, and have a table-ready form that other Components can use. Model never runs storage.

```python
from model import User

user = User(
    name="Ada", username="ada", password="example-password", api_key="example-key"
)

print(user.is_active)  # True: the default of the Activity Field
print(user.id)  # None: pending until storage assigns it
print(user.to_json())
```

## Interface

The package root publishes the Interface contract, version `2.1`, in exactly two forms and nothing else:

- **Entity Export** — every Entity on its own, by its own name, for a consumer that works with one specific Entity.
- **Entity Collection** — `entities`, an immutable tuple holding every Entity once, in Target order, for a consumer that works with all Entities without knowing their names.

Each export and each item of the collection is the actual Entity type. Loading the package creates no instance, data, connection, file, or process. Changing the meaning of the exports, the collection, or an Entity's exposed Declaration raises the contract version and requires a consumer review.

```python
from model import Account  # one Entity, imported directly by its name
from model import entities  # every Entity, in Target order

for entity in entities:
    print(entity.declaration.name)
```

The Entities, in Target order:

### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

Type: `User`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `name` | string | no | — | — | — | — | The user's display name. |
| `username` | string | no | — | — | — | — | The username used to identify the user. |
| `password` | string | no | — | — | — | password | The password credential used by the user. |
| `api_key` | string | no | — | — | — | sensitive | The API key assigned to the user. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the user is active. |
| `description` | string | yes | — | — | — | — | Describes the user. |

- Primary Key: `id`
- Relations: none
- Uniqueness Constraints: (`name`); (`username`)
- Indexes: none

### Trading Platform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

Type: `TradingPlatform`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `name` | string | no | — | — | — | — | The platform's display name. |
| `code` | string | no | — | — | — | — | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the platform is active. |
| `description` | string | yes | — | — | — | — | Describes the platform. |

- Primary Key: `id`
- Relations: none
- Uniqueness Constraints: (`name`)
- Indexes: none

### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

Type: `Instance`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `user_id` | integer | no | — | — | — | — | Identifies the user who owns this instance. |
| `trading_platform_id` | integer | no | — | — | — | — | Identifies the trading platform used by this instance. |
| `name` | string | no | — | — | — | — | The instance's display name. |
| `ip` | string | yes | — | — | — | — | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | string | yes | — | — | — | — | Defines the technical username used to establish the Instance connection when required. |
| `password` | string | yes | — | — | — | password | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | string | yes | — | — | — | sensitive | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the instance is active. |
| `description` | string | yes | — | — | — | — | Describes the instance. |

- Primary Key: `id`
- Relations: `user_id` → `User.id`; `trading_platform_id` → `Trading Platform.id`
- Uniqueness Constraints: (`user_id`, `name`)
- Indexes: none

### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

Type: `Currency`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `user_id` | integer | no | — | — | — | — | Identifies the user who owns this currency. |
| `code` | string | no | — | — | size 3 | — | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | string | yes | — | — | — | — | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | string | yes | — | — | — | — | Identifies the country or region associated with the currency. |
| `decimal_digits` | integer | no | `2` | — | — | — | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the currency is active. |
| `description` | string | yes | — | — | — | — | Describes the currency. |

- Primary Key: `id`
- Relations: `user_id` → `User.id`
- Uniqueness Constraints: (`user_id`, `code`)
- Indexes: none

### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

Type: `Broker`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `name` | string | no | — | — | — | — | The broker's display name. |
| `user_id` | integer | no | — | — | — | — | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the broker is active. |
| `description` | string | yes | — | — | — | — | Describes the broker. |

- Primary Key: `id`
- Relations: `user_id` → `User.id`
- Uniqueness Constraints: (`user_id`, `name`)
- Indexes: none

### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

Type: `Asset`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `broker_id` | integer | no | — | — | — | — | Identifies the broker that provides this asset. |
| `symbol` | string | no | — | — | — | — | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | string | no | — | — | — | — | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | float | no | `0.0` | — | — | — | Stores the size of one point for the asset. |
| `digits` | integer | no | `0` | — | — | — | Stores the number of decimal digits used for the asset's price. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the asset is active. |
| `description` | string | yes | — | — | — | — | Describes the asset. |

- Primary Key: `id`
- Relations: `broker_id` → `Broker.id`
- Uniqueness Constraints: (`broker_id`, `symbol`)
- Indexes: none

### Account Group

Defines an independent group for organizing trading accounts owned by one user.

Type: `AccountGroup`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `user_id` | integer | no | — | — | — | — | Identifies the user who owns the account group. |
| `name` | string | no | — | — | — | — | The account group's display name. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the account group is active. |
| `description` | string | yes | — | — | — | — | Describes the account group. |

- Primary Key: `id`
- Relations: `user_id` → `User.id`
- Uniqueness Constraints: (`user_id`, `name`)
- Indexes: none

### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

Type: `Account`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `name` | string | no | — | — | — | — | The account's display name. |
| `group_id` | integer | no | — | — | — | — | Identifies the account group that contains the account. |
| `broker_id` | integer | no | — | — | — | — | Identifies the broker that owns the account. |
| `instance_id` | integer | no | — | — | — | — | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | no | — | — | — | — | Identifies the base currency used by the account. |
| `username` | string | no | — | — | — | — | The username identifier used to access the trading account. |
| `password` | string | no | — | — | — | password | The credential used to access the trading account. |
| `leverage` | integer | no | — | — | — | — | Defines the account's leverage multiplier. |
| `balance` | decimal | no | `0` | — | — | — | Stores the account's current balance. |
| `account_type` | string | no | — | — | — | — | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the account is active. |
| `description` | string | yes | — | — | — | — | Describes the account. |

- Primary Key: `id`
- Relations: `group_id` → `Account Group.id`; `broker_id` → `Broker.id`; `instance_id` → `Instance.id`; `base_currency_id` → `Currency.id`
- Uniqueness Constraints: (`name`); (`group_id`, `broker_id`, `instance_id`)
- Indexes: none

### Trailing Group

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

Type: `TrailingGroup`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `user_id` | integer | no | — | — | — | — | Identifies the user who owns the trailing group. |
| `name` | string | no | — | — | — | — | The trailing group's display name. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the trailing group is active. |
| `description` | string | yes | — | — | — | — | Describes the trailing group. |

- Primary Key: `id`
- Relations: `user_id` → `User.id`
- Uniqueness Constraints: (`user_id`, `name`)
- Indexes: none

### Trailing Rule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

Type: `TrailingRule`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `name` | string | no | — | — | — | — | The trailing rule's display name. |
| `trailing_group_id` | integer | no | — | — | — | — | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | decimal | no | — | — | — | — | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | decimal | yes | — | — | — | — | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | decimal | yes | — | — | — | — | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the trailing rule is active. |
| `description` | string | yes | — | — | — | — | Describes the trailing rule. |

- Primary Key: `id`
- Relations: `trailing_group_id` → `Trailing Group.id`
- Uniqueness Constraints: (`name`); (`trailing_group_id`, `trigger_percentage`)
- Indexes: none

### Partial Group

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

Type: `PartialGroup`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `user_id` | integer | no | — | — | — | — | Identifies the user who owns the partial group. |
| `name` | string | no | — | — | — | — | The partial group's display name. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the partial group is active. |
| `description` | string | yes | — | — | — | — | Describes the partial group. |

- Primary Key: `id`
- Relations: `user_id` → `User.id`
- Uniqueness Constraints: (`user_id`, `name`)
- Indexes: none

### Partial Rule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

Type: `PartialRule`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `name` | string | no | — | — | — | — | The partial rule's display name. |
| `partial_group_id` | integer | no | — | — | — | — | Identifies the partial group that contains the rule. |
| `profit_percentage` | decimal | no | — | — | — | — | Defines the profit percentage that activates the rule. |
| `close_percentage` | decimal | no | — | — | — | — | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the partial rule is active. |
| `description` | string | yes | — | — | — | — | Describes the partial rule. |

- Primary Key: `id`
- Relations: `partial_group_id` → `Partial Group.id`
- Uniqueness Constraints: (`name`); (`partial_group_id`, `profit_percentage`)
- Indexes: none

### Action Group

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

Type: `ActionGroup`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `user_id` | integer | no | — | — | — | — | Identifies the user who owns the action group. |
| `name` | string | no | — | — | — | — | The action group's display name. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the action group is active. |
| `description` | string | yes | — | — | — | — | Describes the action group. |

- Primary Key: `id`
- Relations: `user_id` → `User.id`
- Uniqueness Constraints: (`user_id`, `name`)
- Indexes: none

### Action

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

Type: `Action`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `name` | string | no | — | — | — | — | The action's display name. |
| `action_group_id` | integer | no | — | — | — | — | Identifies the action group that contains the action. |
| `asset_id` | integer | no | — | — | — | — | Identifies the asset traded by the action. |
| `account_id` | integer | no | — | — | — | — | Identifies the account used to execute the action. |
| `partial_group_id` | integer | no | — | — | — | — | Identifies the Partial Group used by the action. |
| `trailing_group_id` | integer | no | — | — | — | — | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | decimal | no | — | — | — | — | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | decimal | no | — | — | — | — | Defines the Take Profit value used by the action. |
| `stop_loss` | decimal | no | — | — | — | — | Defines the Stop Loss value used by the action. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the action is active. |
| `description` | string | yes | — | — | — | — | Describes the action. |

- Primary Key: `id`
- Relations: `action_group_id` → `Action Group.id`; `asset_id` → `Asset.id`; `account_id` → `Account.id`; `partial_group_id` → `Partial Group.id`; `trailing_group_id` → `Trailing Group.id`
- Uniqueness Constraints: (`action_group_id`, `name`)
- Indexes: none

### Position

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

Type: `Position`

| Field | Type | Nullable | Default | Generation | Constraints | Sensitivity | Description |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | integer | no | — | auto_increment | immutable | — | — |
| `user_id` | integer | no | — | — | — | — | Identifies the user who owns the position. |
| `name` | string | no | — | — | — | — | The position's display name. |
| `trading_platform_id` | integer | no | — | — | — | — | Identifies the trading platform used to execute the position. |
| `broker_id` | integer | no | — | — | — | — | Identifies the broker through which the position is executed. |
| `account_id` | integer | no | — | — | — | — | Identifies the trading account used for the position. |
| `trailing_group_id` | integer | no | — | — | — | — | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | integer | no | — | — | — | — | Identifies the Partial Group applied to the position. |
| `action_group_id` | integer | no | — | — | — | — | Identifies the Action Group associated with the position. |
| `action_id` | integer | no | — | — | — | — | Identifies the action from which the position is created. |
| `date` | datetime | no | — | — | — | — | Stores the position's date and time. |
| `volume` | decimal | no | — | — | — | — | Stores the position's trading volume. |
| `profit` | decimal | no | `0` | — | — | — | Stores the position's current profit or loss. |
| `is_executed` | boolean | no | `false` | — | — | — | Indicates whether the position has been executed. |
| `order_type` | string | no | — | — | — | — | Stores the position's order type. |
| `base_tp` | decimal | no | — | — | — | — | Stores the position's initial Take Profit value. |
| `base_sl` | decimal | no | — | — | — | — | Stores the position's initial Stop Loss value. |
| `real_tp` | decimal | no | — | — | — | — | Stores the position's current Take Profit value. |
| `real_sl` | decimal | no | — | — | — | — | Stores the position's current Stop Loss value. |
| `is_active` | boolean | no | `true` | — | — | — | Indicates whether the position is active. |
| `description` | string | yes | — | — | — | — | Describes the position. |

- Primary Key: `id`
- Relations: `user_id` → `User.id`; `trading_platform_id` → `Trading Platform.id`; `broker_id` → `Broker.id`; `account_id` → `Account.id`; `trailing_group_id` → `Trailing Group.id`; `partial_group_id` → `Partial Group.id`; `action_group_id` → `Action Group.id`; `action_id` → `Action.id`
- Uniqueness Constraints: (`name`)
- Indexes: none

## Declaration

Every Entity exposes its public Declaration as the class attribute `declaration`. A Declaration is an immutable record; its Fields keep Declaration order.

```python
from model import Account

declaration = Account.declaration

print(declaration.name)  # Account
print(declaration.description)
print([field.name for field in declaration.fields])
print(declaration.primary_key)  # id
# Relation records: local_field, target_entity, target_field
print(declaration.relations)
print(declaration.unique_constraints)  # fields of each Uniqueness Constraint
print(declaration.indexes)

balance = declaration.field("balance")
print(balance.type, balance.nullable, balance.default, balance.sensitivity)
print(balance.immutable, balance.constraints, balance.value_generation)
```

An absent Default Value (`NO_DEFAULT`) differs from an explicit `None` default. The Declaration types are importable from `model.core.declaration`.

## Foundation

Every Entity extends Foundation, which gives it conversion to and from JSON text. The text is standard JSON with one root object whose keys are exactly the Entity's Field names, in Declaration order.

`to_json()` returns that text. A pending `id` and any null value are written as `null`; a decimal is written as exact text; a datetime is written as ISO 8601 text with its offset; a uuid is written as text.

```python
from decimal import Decimal

from model import TrailingRule

rule = TrailingRule(
    name="Rule 1", trailing_group_id=1, trigger_percentage=Decimal("12.50")
)
print(rule.to_json())  # "trigger_percentage": "12.50" keeps its exact text
```

`from_json(text)` builds an Entity from such text with the same rules as direct construction. It rejects malformed text, a repeated key, a non-standard constant (`NaN`, `Infinity`), and a root that is not one object, then decodes each value by its Field's Type.

```python
from model import Currency

restored = Currency.from_json('{"user_id": 1, "code": "EUR", "symbol": "€"}')
print(restored.decimal_digits)  # 2: an absent key applies the default
```

A complete round trip, Entity to JSON text to Entity:

```python
from model import Currency

original = Currency(
    user_id=1, code="JPY", symbol="¥", country="Japan", decimal_digits=0
)
text = original.to_json()
restored = Currency.from_json(text)

assert restored.to_json() == text
assert restored.decimal_digits == 0  # zero stays distinct from null
assert restored.description is None
```

An Auto Increment Field is closed to callers, so text that carries a value for `id` is refused; `null` is accepted and leaves `id` pending.

## Setup

Model is a Python library managed with `uv`.

1. Install Python 3.14 or newer and `uv`.
2. In the Component root, create the isolated environment from the lockfile:

   ```text
   uv sync
   ```

3. Confirm the package loads:

   ```text
   uv run python -c "import model; print(len(model.entities))"
   ```

   It prints `15`.

A consumer in the same repository depends on this directory as a local path dependency, never as a published package:

```toml
[project]
dependencies = ["model"]

[tool.uv.sources]
model = { path = "../model" }
```

## Use

Use Model only through the Entity exports and the Entity Collection.

```python
from model import Currency, entities

currency = Currency(user_id=1, code="USD", symbol="$")

currency.symbol = "US$"  # a valid assignment changes the value
try:
    currency.code = "TOOLONG"  # the whole Entity is revalidated first
except ValueError:
    print("refused; code is still", currency.code)

for entity in entities:
    print(entity.declaration.name, len(entity.declaration.fields), "fields")
```

Construction accepts only declared Fields and never converts a value: a text value for a decimal Field, an integer for a boolean Field, or a datetime without a timezone is refused. The `id` Field is assigned by storage and is refused if supplied. Assignment to an immutable Field is refused.

Every Entity has a table-ready form. All of them are registered in one shared table metadata, which a consumer reaches through the Entities themselves; Model never opens a connection or creates a table.

```python
from model import entities

print(sorted(entities[0].metadata.tables))  # the 15 tables of the 15 Entities
```

## Verify

Run this from the Component root with `uv run python verify.py`, after saving it as `verify.py` outside the package (it is a check you run, not part of the library). It exits with an error at the first observation that does not hold.

```python
import os
import subprocess
import sys
import tempfile
import types
from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import model
from model.core.foundation import Foundation

NAMES = [
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


def refused(action, *errors):
    try:
        action()
    except errors:
        return
    raise AssertionError("accepted what the contract refuses")


# Interface shape and exact Entity Export membership: the Entities and the collection, nothing else.
public = [
    n
    for n in dir(model)
    if not n.startswith("_") and not isinstance(getattr(model, n), types.ModuleType)
]
assert sorted(public) == sorted(NAMES + ["entities"])

# Entity Collection membership and order, and its correspondence with the exports.
assert isinstance(model.entities, tuple)
assert [entity.__name__ for entity in model.entities] == NAMES
assert all(getattr(model, entity.__name__) is entity for entity in model.entities)

# Actual Entity and Declaration references.
for entity in model.entities:
    assert (
        issubclass(entity, Foundation)
        and entity.declaration is entity.__dict__["declaration"]
    )

# Immutability: the collection, the Declaration, and the Identity.
refused(lambda: model.entities.append(model.User), AttributeError)
refused(lambda: setattr(model.User.declaration, "name", "x"), FrozenInstanceError)

# Side-effect freedom: loading creates nothing.
with tempfile.TemporaryDirectory() as empty:
    subprocess.run([sys.executable, "-B", "-c", "import model"], cwd=empty, check=True)
    assert os.listdir(empty) == []

# Declaration access: Fields, Primary Key, Relations, Uniqueness Constraints, Indexes.
declaration = model.Position.declaration
assert declaration.field_names[0] == "id" and declaration.primary_key == "id"
assert (
    len(declaration.relations) == 8
    and declaration.unique_constraints
    and declaration.indexes == ()
)

# Representative construction, and refusal of what the contract refuses.
user = model.User(
    name="Ada", username="ada", password="example-password", api_key="example-key"
)
assert user.id is None and user.is_active is True
refused(
    lambda: model.User(
        name="Ada", username="ada", password="x", api_key="y", unknown=1
    ),
    ValueError,
)
refused(
    lambda: model.User(name=1, username="ada", password="x", api_key="y"), ValueError
)
refused(lambda: model.User(username="ada", password="x", api_key="y"), ValueError)
refused(
    lambda: model.User(name="Ada", username="ada", password="x", api_key="y", id=1),
    ValueError,
)
refused(lambda: setattr(user, "id", 1), ValueError)

# Lossless JSON text round trip, with exact decimal and datetime values.
position = model.Position(
    user_id=1,
    name="P-1",
    trading_platform_id=1,
    broker_id=1,
    account_id=1,
    trailing_group_id=1,
    partial_group_id=1,
    action_group_id=1,
    action_id=1,
    date=datetime(2026, 3, 4, 5, 6, 7, tzinfo=timezone(timedelta(hours=9))),
    volume=Decimal("0.10"),
    order_type="buy",
    base_tp=Decimal("1.10000"),
    base_sl=Decimal("1.00000"),
    real_tp=Decimal("1.10000"),
    real_sl=Decimal("1.00000"),
)
text = position.to_json()
restored = model.Position.from_json(text)
assert restored.to_json() == text
assert restored.volume == Decimal("0.10") and str(restored.volume) == "0.10"
assert restored.date == position.date and restored.date.utcoffset() == timedelta(
    hours=9
)

print("Model verified")
```

## Troubleshooting

These cover Model only.

| You see | Cause | What to do |
| --- | --- | --- |
| A validation error naming `extra_forbidden` | A value was given for a Field the Entity does not declare. | Use only the Fields of the Entity's Declaration. |
| A validation error such as "Input should be …" | Model never converts values: text or float for a decimal, an integer for a boolean, a naive datetime. | Pass the exact Type: `Decimal`, `bool`, a timezone-aware `datetime`. |
| A validation error naming `none_required` on `id` | `id` is assigned by storage and cannot be supplied. | Omit `id`, or pass `None`. |
| An assignment error saying a Field is immutable or closed to callers | The Field is the Identity or an Auto Increment Field. | Do not assign it. |
| A refused assignment leaves the old value | Assignment revalidates the whole Entity first and only then changes it. | Fix the new value. |
| `[redacted]` where a value would be | A Field carries a Sensitivity Marker, so its input is never printed in a message. | Expected; the stored value is unchanged. |
| `unhashable type` | A mutable Entity cannot be hashed. | Key by `id` or by a Field value. |
| `AttributeError` appending to `entities` | The collection is an immutable tuple. | Build your own list from it. |
| A `ValueError` from `from_json` | The text is malformed, repeats a key, holds `NaN` or `Infinity`, is not one object, or has a value of the wrong form. | Produce the text with `to_json()` or match its forms. |
| An error when the package loads naming a type, table, or Field | An Entity type disagrees with its Declaration, a Declaration is contradictory, a name cannot be resolved, or a Relation does not resolve. | Correct the Target or Declaration; loading stops instead of guessing, and an unknown Field Type is never guessed. |

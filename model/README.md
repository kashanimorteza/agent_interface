# Model

## Overview

Model is the reusable data library of the Trading Assistant. It defines 15 flat, technology-independent
Entities. Each Entity carries its own Fields, Entity Metadata, and public Declaration, converts to and
from JSON text, and rejects any value its Fields do not allow.

```python
from model.interface import User

user = User(name="Admin", username="admin", password="example-password", api_key="example-key")
print(user.is_active)  # True: the default
print(user.id)  # None: pending until storage generates it
```

## Interface

`model.interface` is the only entry point. It publishes exactly two things:

- **Entity Exports** — one explicit named export for every Entity, each being the actual Entity. An export is
  named by the Entity's physical name: its logical name in PascalCase without spaces.
- **Entity Collection** — `entities`, an immutable tuple holding every actual Entity once, in Target order.

Nothing else is published, and loading the Interface creates no Entity instance, data, connection, file, or
process.

Import one Entity directly:

```python
from model.interface import TradingPlatform
```

Enumerate every Entity:

```python
from model.interface import entities

for entity in entities:
    print(entity.declaration.name)
```

Every Entity has an immutable `id` Field (Auto Increment, pending until storage assigns it) and a mutable
Boolean `is_active` Field, as the tables below show. The Entities appear in Target order.

### User

Exported as `User`. Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `name` | string | no | none | — | The user's display name. |
| `username` | string | no | none | — | The username used to identify the user. |
| `password` | string | no | none | — | The password credential used by the user. |
| `api_key` | string | no | none | — | The API key assigned to the user. |
| `is_active` | boolean | no | `true` | — | Indicates whether the user is active. |
| `description` | string | yes | none | — | Describes the user. |

Entity Metadata:

- Primary Key: `id`
- Relations: none
- Uniqueness Constraint: `name`
- Uniqueness Constraint: `username`
- Indexes: none

### Trading Platform

Exported as `TradingPlatform`. Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `name` | string | no | none | — | The platform's display name. |
| `code` | string | no | none | — | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | boolean | no | `true` | — | Indicates whether the platform is active. |
| `description` | string | yes | none | — | Describes the platform. |

Entity Metadata:

- Primary Key: `id`
- Relations: none
- Uniqueness Constraint: `name`
- Indexes: none

### Instance

Exported as `Instance`. Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `user_id` | integer | no | none | — | Identifies the user who owns this instance. |
| `trading_platform_id` | integer | no | none | — | Identifies the trading platform used by this instance. |
| `name` | string | no | none | — | The instance's display name. |
| `ip` | string | yes | none | — | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | string | yes | none | — | Defines the technical username used to establish the Instance connection when required. |
| `password` | string | yes | none | — | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | string | yes | none | — | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | no | `true` | — | Indicates whether the instance is active. |
| `description` | string | yes | none | — | Describes the instance. |

Entity Metadata:

- Primary Key: `id`
- Relation: `user_id` → User.`id`
- Relation: `trading_platform_id` → Trading Platform.`id`
- Uniqueness Constraint: `user_id`, `name`
- Indexes: none

### Currency

Exported as `Currency`. Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `user_id` | integer | no | none | — | Identifies the user who owns this currency. |
| `code` | string | no | none | size 3 | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | string | yes | none | — | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | string | yes | none | — | Identifies the country or region associated with the currency. |
| `decimal_digits` | integer | no | `2` | — | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | no | `true` | — | Indicates whether the currency is active. |
| `description` | string | yes | none | — | Describes the currency. |

Entity Metadata:

- Primary Key: `id`
- Relation: `user_id` → User.`id`
- Uniqueness Constraint: `user_id`, `code`
- Indexes: none

### Broker

Exported as `Broker`. Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `name` | string | no | none | — | The broker's display name. |
| `user_id` | integer | no | none | — | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | no | `true` | — | Indicates whether the broker is active. |
| `description` | string | yes | none | — | Describes the broker. |

Entity Metadata:

- Primary Key: `id`
- Relation: `user_id` → User.`id`
- Uniqueness Constraint: `user_id`, `name`
- Indexes: none

### Asset

Exported as `Asset`. Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `broker_id` | integer | no | none | — | Identifies the broker that provides this asset. |
| `symbol` | string | no | none | — | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | string | no | none | — | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | float | no | `0.0` | — | Stores the size of one point for the asset. |
| `digits` | integer | no | `0` | — | Stores the number of decimal digits used for the asset's price. |
| `is_active` | boolean | no | `true` | — | Indicates whether the asset is active. |
| `description` | string | yes | none | — | Describes the asset. |

Entity Metadata:

- Primary Key: `id`
- Relation: `broker_id` → Broker.`id`
- Uniqueness Constraint: `broker_id`, `symbol`
- Indexes: none

### Account Group

Exported as `AccountGroup`. Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `user_id` | integer | no | none | — | Identifies the user who owns the account group. |
| `name` | string | no | none | — | The account group's display name. |
| `is_active` | boolean | no | `true` | — | Indicates whether the account group is active. |
| `description` | string | yes | none | — | Describes the account group. |

Entity Metadata:

- Primary Key: `id`
- Relation: `user_id` → User.`id`
- Uniqueness Constraint: `user_id`, `name`
- Indexes: none

### Account

Exported as `Account`. Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `name` | string | no | none | — | The account's display name. |
| `group_id` | integer | no | none | — | Identifies the account group that contains the account. |
| `broker_id` | integer | no | none | — | Identifies the broker that owns the account. |
| `instance_id` | integer | no | none | — | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | no | none | — | Identifies the base currency used by the account. |
| `username` | string | no | none | — | The username identifier used to access the trading account. |
| `password` | string | no | none | — | The credential used to access the trading account. |
| `leverage` | integer | no | none | — | Defines the account's leverage multiplier. |
| `balance` | decimal | no | `0` | — | Stores the account's current balance. |
| `account_type` | string | no | none | — | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | boolean | no | `true` | — | Indicates whether the account is active. |
| `description` | string | yes | none | — | Describes the account. |

Entity Metadata:

- Primary Key: `id`
- Relation: `group_id` → Account Group.`id`
- Relation: `broker_id` → Broker.`id`
- Relation: `instance_id` → Instance.`id`
- Relation: `base_currency_id` → Currency.`id`
- Uniqueness Constraint: `name`
- Uniqueness Constraint: `group_id`, `broker_id`, `instance_id`
- Indexes: none

### Trailing Group

Exported as `TrailingGroup`. Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `user_id` | integer | no | none | — | Identifies the user who owns the trailing group. |
| `name` | string | no | none | — | The trailing group's display name. |
| `is_active` | boolean | no | `true` | — | Indicates whether the trailing group is active. |
| `description` | string | yes | none | — | Describes the trailing group. |

Entity Metadata:

- Primary Key: `id`
- Relation: `user_id` → User.`id`
- Uniqueness Constraint: `user_id`, `name`
- Indexes: none

### Trailing Rule

Exported as `TrailingRule`. Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `name` | string | no | none | — | The trailing rule's display name. |
| `trailing_group_id` | integer | no | none | — | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | decimal | no | none | — | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | decimal | yes | none | — | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | decimal | yes | none | — | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | boolean | no | `true` | — | Indicates whether the trailing rule is active. |
| `description` | string | yes | none | — | Describes the trailing rule. |

Entity Metadata:

- Primary Key: `id`
- Relation: `trailing_group_id` → Trailing Group.`id`
- Uniqueness Constraint: `name`
- Uniqueness Constraint: `trailing_group_id`, `trigger_percentage`
- Indexes: none

### Partial Group

Exported as `PartialGroup`. Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `user_id` | integer | no | none | — | Identifies the user who owns the partial group. |
| `name` | string | no | none | — | The partial group's display name. |
| `is_active` | boolean | no | `true` | — | Indicates whether the partial group is active. |
| `description` | string | yes | none | — | Describes the partial group. |

Entity Metadata:

- Primary Key: `id`
- Relation: `user_id` → User.`id`
- Uniqueness Constraint: `user_id`, `name`
- Indexes: none

### Partial Rule

Exported as `PartialRule`. Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `name` | string | no | none | — | The partial rule's display name. |
| `partial_group_id` | integer | no | none | — | Identifies the partial group that contains the rule. |
| `profit_percentage` | decimal | no | none | — | Defines the profit percentage that activates the rule. |
| `close_percentage` | decimal | no | none | — | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | boolean | no | `true` | — | Indicates whether the partial rule is active. |
| `description` | string | yes | none | — | Describes the partial rule. |

Entity Metadata:

- Primary Key: `id`
- Relation: `partial_group_id` → Partial Group.`id`
- Uniqueness Constraint: `name`
- Uniqueness Constraint: `partial_group_id`, `profit_percentage`
- Indexes: none

### Action Group

Exported as `ActionGroup`. Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `user_id` | integer | no | none | — | Identifies the user who owns the action group. |
| `name` | string | no | none | — | The action group's display name. |
| `is_active` | boolean | no | `true` | — | Indicates whether the action group is active. |
| `description` | string | yes | none | — | Describes the action group. |

Entity Metadata:

- Primary Key: `id`
- Relation: `user_id` → User.`id`
- Uniqueness Constraint: `user_id`, `name`
- Indexes: none

### Action

Exported as `Action`. Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `name` | string | no | none | — | The action's display name. |
| `action_group_id` | integer | no | none | — | Identifies the action group that contains the action. |
| `asset_id` | integer | no | none | — | Identifies the asset traded by the action. |
| `account_id` | integer | no | none | — | Identifies the account used to execute the action. |
| `partial_group_id` | integer | no | none | — | Identifies the Partial Group used by the action. |
| `trailing_group_id` | integer | no | none | — | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | decimal | no | none | — | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | decimal | no | none | — | Defines the Take Profit value used by the action. |
| `stop_loss` | decimal | no | none | — | Defines the Stop Loss value used by the action. |
| `is_active` | boolean | no | `true` | — | Indicates whether the action is active. |
| `description` | string | yes | none | — | Describes the action. |

Entity Metadata:

- Primary Key: `id`
- Relation: `action_group_id` → Action Group.`id`
- Relation: `asset_id` → Asset.`id`
- Relation: `account_id` → Account.`id`
- Relation: `partial_group_id` → Partial Group.`id`
- Relation: `trailing_group_id` → Trailing Group.`id`
- Uniqueness Constraint: `action_group_id`, `name`
- Indexes: none

### Position

Exported as `Position`. Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Nullable | Default | Notes | Description |
|---|---|---|---|---|---|
| `id` | integer | no | none | Auto Increment, pending (`None`) until storage assigns it; immutable | — |
| `user_id` | integer | no | none | — | Identifies the user who owns the position. |
| `name` | string | no | none | — | The position's display name. |
| `trading_platform_id` | integer | no | none | — | Identifies the trading platform used to execute the position. |
| `broker_id` | integer | no | none | — | Identifies the broker through which the position is executed. |
| `account_id` | integer | no | none | — | Identifies the trading account used for the position. |
| `trailing_group_id` | integer | no | none | — | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | integer | no | none | — | Identifies the Partial Group applied to the position. |
| `action_group_id` | integer | no | none | — | Identifies the Action Group associated with the position. |
| `action_id` | integer | no | none | — | Identifies the action from which the position is created. |
| `date` | datetime | no | none | — | Stores the position's date and time. |
| `volume` | decimal | no | none | — | Stores the position's trading volume. |
| `profit` | decimal | no | `0` | — | Stores the position's current profit or loss. |
| `is_executed` | boolean | no | `false` | — | Indicates whether the position has been executed. |
| `order_type` | string | no | none | — | Stores the position's order type. |
| `base_tp` | decimal | no | none | — | Stores the position's initial Take Profit value. |
| `base_sl` | decimal | no | none | — | Stores the position's initial Stop Loss value. |
| `real_tp` | decimal | no | none | — | Stores the position's current Take Profit value. |
| `real_sl` | decimal | no | none | — | Stores the position's current Stop Loss value. |
| `is_active` | boolean | no | `true` | — | Indicates whether the position is active. |
| `description` | string | yes | none | — | Describes the position. |

Entity Metadata:

- Primary Key: `id`
- Relation: `user_id` → User.`id`
- Relation: `trading_platform_id` → Trading Platform.`id`
- Relation: `broker_id` → Broker.`id`
- Relation: `account_id` → Account.`id`
- Relation: `trailing_group_id` → Trailing Group.`id`
- Relation: `partial_group_id` → Partial Group.`id`
- Relation: `action_group_id` → Action Group.`id`
- Relation: `action_id` → Action.`id`
- Uniqueness Constraint: `name`
- Indexes: none

## Declaration

Every Entity exposes its complete public Declaration as the class attribute `declaration`. It is read-only and
holds no behaviour.

```python
from model.interface import Instance

declaration = Instance.declaration
print(declaration.name, "-", declaration.description)

for field in declaration.fields:
    print(field.name, field.type.value, field.nullable, field.has_default, field.default)

print(declaration.primary_key)  # id
for relation in declaration.relations:
    print(relation.local_field, "->", relation.target_entity, relation.target_field)
for unique in declaration.unique_constraints:
    print("unique:", unique.fields)
print(declaration.indexes)  # ()
```

A Field Declaration exposes `name`, `type`, `nullable`, `description`, `has_default`, `default`,
`sensitivity`, `immutable`, `constraints` (its `size`), and `value_generation`. `has_default` tells an absent
Default Value from an explicit `None` default. Logical names, such as `Trading Platform`, are kept exactly as
the Target spells them in every Declaration.

## Foundation

Every Entity provides two conversions between itself and its JSON Object: JSON text with one root object whose
keys are exactly the Entity's Field names, in Declaration order.

`to_json` returns the text:

```python
from model.interface import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(currency.to_json())
```

`from_json` reconstructs an Entity from the text, enforcing the same rules as direct construction:

```python
text = '{"id": null, "user_id": 1, "code": "EUR", "symbol": null, "country": null, "decimal_digits": 2, "is_active": true, "description": null}'
euro = Currency.from_json(text)
print(euro.code)  # EUR
```

A complete round trip, Entity to JSON text and back:

```python
from decimal import Decimal

from model.interface import Account

account = Account(
    name="Acc-1",
    group_id=1,
    broker_id=1,
    instance_id=1,
    base_currency_id=1,
    username="test",
    password="example-password",
    leverage=100,
    balance=Decimal("1250.50"),
    account_type="CFD",
)
restored = Account.from_json(account.to_json())
assert restored == account
assert restored.balance == Decimal("1250.50")
```

Decimals travel as exact text, datetimes as ISO 8601 text with an offset, and a pending `id` as `null`.

## Setup

Requirements: Python 3.14 or newer and [uv](https://docs.astral.sh/uv/).

```sh
cd model
uv sync
```

`uv sync` creates the isolated environment in `.venv` from `pyproject.toml` and `uv.lock`. Run Python in it with
`uv run python`. The Model depends on SQLModel, Pydantic, and SQLAlchemy; `ruff` and `pyright` are development
tools.

## Use

Construct an Entity with keyword values. Only declared Fields are accepted, values are never coerced, and a
Field you omit takes its default:

```python
from model.interface import Broker

broker = Broker(name="FxPro", user_id=1)
print(broker.is_active)  # True
```

Assign a mutable Field. The whole Entity is revalidated, and a rejected assignment keeps the previous value:

```python
broker.name = "Another broker"
try:
    broker.name = 5
except ValueError:
    print(broker.name)  # Another broker
```

Read a Declaration or enumerate every Entity through the Entity Collection:

```python
from model.interface import entities

for entity in entities:
    print(entity.declaration.name, [field.name for field in entity.declaration.fields][:3])
```

An Entity is mutable, so it is not hashable. The `id` Field is generated outside the Model: leave it out (or
`None`) and it stays pending.

## Verify

This script checks the published shape and the main behaviours. Run it with `uv run python`. It prints
`all checks passed` when every check holds.

```python
import json
import subprocess
import sys
from datetime import datetime, timezone
from decimal import Decimal

from model import interface
from model.interface import Position, entities

EXPECTED_ORDER = [
    "User",
    "Trading Platform",
    "Instance",
    "Currency",
    "Broker",
    "Asset",
    "Account Group",
    "Account",
    "Trailing Group",
    "Trailing Rule",
    "Partial Group",
    "Partial Rule",
    "Action Group",
    "Action",
    "Position",
]

exports = sorted(name for name in vars(interface) if not name.startswith("_") and name != "entities")

# Exact Entity Export membership; the Entity Collection holds the same Entities, once, in order.
assert len(exports) == len(entities) == 15
assert exports == sorted(entity.__name__ for entity in entities)
assert all(getattr(interface, entity.__name__) is entity for entity in entities)
assert isinstance(entities, tuple)
assert [entity.declaration.name for entity in entities] == EXPECTED_ORDER

# Each export is the actual Entity and exposes its actual Declaration, which is read-only.
for entity in entities:
    assert entity.declaration.primary_key == "id"
    assert list(entity.model_fields) == [field.name for field in entity.declaration.fields]
    try:
        entity.declaration.name = "changed"
    except AttributeError:
        pass
    else:
        raise AssertionError("Declaration is not read-only")

# Construction, strictness, and the immutable id.
position = Position(
    user_id=1,
    name="P-1",
    trading_platform_id=1,
    broker_id=1,
    account_id=1,
    trailing_group_id=1,
    partial_group_id=1,
    action_group_id=1,
    action_id=1,
    date=datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
    volume=Decimal("0.10"),
    order_type="buy",
    base_tp=Decimal("1.2"),
    base_sl=Decimal("1.1"),
    real_tp=Decimal("1.2"),
    real_sl=Decimal("1.1"),
)
assert position.id is None and position.is_active is True and position.profit == Decimal("0")
for invalid in ({"volume": 0.1}, {"unknown": 1}, {"id": 1}):
    try:
        Position(**{**position.model_dump(exclude={"id"}), **invalid})
    except ValueError:
        pass
    else:
        raise AssertionError(f"accepted {invalid}")
try:
    position.id = 7
except ValueError:
    pass
else:
    raise AssertionError("id is assignable")

# Loading the Interface has no side effect: no file written, connection, process, or Entity created.
PROBE = '''
import gc
import sys

events = []


def hook(event, args):
    if event in ("socket.connect", "subprocess.Popen", "os.system", "sqlite3.connect"):
        events.append(event)
    if event == "open" and any(mode in str(args[1]) for mode in "wax+"):
        events.append(event)


sys.addaudithook(hook)
import model.interface as interface

instances = [obj for obj in gc.get_objects() if type(obj) in interface.entities]
assert not events and not instances, (events, len(instances))
'''
subprocess.run([sys.executable, "-B", "-c", PROBE], check=True)

# A lossless JSON text round trip.
text = position.to_json()
assert list(json.loads(text)) == [field.name for field in Position.declaration.fields]
assert Position.from_json(text) == position
assert Position.from_json(text).to_json() == text

print("all checks passed")
```

## Troubleshooting

- **`ValidationError` when constructing or assigning.** Values are validated strictly and never coerced: text for
  an integer, a float for a decimal, an integer for a boolean, and a datetime without timezone information are all
  refused. Pass the declared Type. An unknown Field name and a missing required value are refused too.
- **`ValueError: <Entity>.id is generated`.** An Auto Increment Field cannot be supplied on construction or in JSON
  text; omit it, or pass `None` for it, and it stays pending until storage assigns it.
- **`ValueError: <Entity>.id is immutable`.** Assigning the `id` Field is refused. Only `id` is immutable, and an
  immutable Field cannot be assigned.
- **`TypeError: unhashable type`.** Entities are mutable and are not hashable.
- **`from_json` raises.** The text must be standard JSON with one root object, each key once, no `NaN` or
  `Infinity`, decimals as text, and datetimes as ISO 8601 text with an offset. Every other rule is the one that
  direct construction applies, including a `null` `id`.
- **`ModuleNotFoundError: No module named 'model'`.** Run Python inside the Model's environment, from the Model
  directory, with `uv run python`.

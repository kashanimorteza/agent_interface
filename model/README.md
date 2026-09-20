# Model

The shared domain Model of the Trading Assistant: one authoritative Domain Definition for every
concept the Target defines, published through one Public Interface.

## Overview

**What it is.** A reusable Python package, independent of every other Application Package. It
defines what a `User`, `Instance`, `Currency`, `Broker`, `Asset`, `Account`, `Position` and the
other Target concepts *are*: their Fields, relationships and the rules that can be checked from a
record's own data.

**What it does.** It lets a consumer build a validated record, convert it to plain values and
back, and read exactly what a definition declares — type, length, whether a value may be absent,
defaults, identity, uniqueness, credential classification, persistence and relationships.

**What it does not do.** Model stores nothing, performs no application behaviour, and offers no
stored-data operation (no save, load, update or delete). It holds no Initial Data: the Target's
initial records are delivered by the Database phase. It never applies a credential's at-rest
treatment; it only states it.

**Where it sits.** Database, Logic, API and Presentation consume it: they take the definitions and
the declarations from here rather than defining their own.

## Public Interface

Everything is reached from one entry point, `model`.

```text
model
├── Operations
│   ├── describe(definition)                → Declaration
│   ├── create(definition, **values)        → instance
│   ├── serialize(instance)                 → Plain Representation
│   └── deserialize(definition, data)       → instance
├── Domain Definitions (15)
│   User · TradingPlatform · Instance · Currency · Broker · Asset · AccountGroup · Account
│   TrailingGroup · TrailingRule · PartialGroup · PartialRule · ActionGroup · Action · Position
├── Declaration vocabulary
│   Declaration · FieldDeclaration · Relationship · Precision · Persistence · Cardinality · AtRest
│   Identity · Generated · Unique · Activation · Credential
└── Shared types
    ModelFoundation · ExactDecimal · Instant
```

Every Operation reports a bad input as `pydantic.ValidationError` (naming each offending Field) or,
when the first argument is not a Domain Definition, `TypeError`.

### How values are checked

- **Strict types.** `"1"` is not an integer and `1` is not a boolean. Text is accepted only for
  exact decimals and instants, so a Plain Representation parses back.
- **Exact decimals** take text or integers (`"0.10"`, `5`), never a floating point number, `NaN`
  or infinity.
- **Instants** must carry a timezone; they are normalised to UTC.
- **Optional Fields** have no default: supply `None` explicitly.
- **Generated Fields** (`id`) have no value until something else produces one; leave them out.
- **Unknown names** are refused. Text has surrounding whitespace removed.
- **Assignment** to an existing instance is validated the same way.

### Operations

#### `describe(definition) -> Declaration`

Accepts a Domain Definition. Returns its `Declaration`: `name`, `persistence`, `fields`
(each a `FieldDeclaration`), `relationships` (each carries the referenced definition itself) and
`unique_sets`. Raises `TypeError` for anything that is not a Domain Definition.

```python
from model import Account, describe

declaration = describe(Account)
print(declaration.persistence, [f.name for f in declaration.fields][:3])
for relationship in declaration.relationships:
    print(relationship.name, "->", relationship.reference.__name__, relationship.cardinality)
```

#### `create(definition, **values) -> instance`

Accepts a Domain Definition and one named value per Field it requires. Returns the validated
instance. Raises `ValidationError` for a missing, unknown or invalid value.

```python
from model import Broker, create

broker = create(Broker, name="FxPro", user_id=1, description=None)
print(broker.is_active, broker.id)
```

#### `serialize(instance) -> dict`

Accepts an instance. Returns every Field as a simple, JSON-compatible value; nothing is withheld
and a relationship appears only as its reference value. Raises `TypeError` for a non-instance.

```python
import json

from model import Broker, serialize

plain = serialize(Broker(name="FxPro", user_id=1, description=None))
print(json.dumps(plain))
```

#### `deserialize(definition, data) -> instance`

Accepts a Domain Definition and its Plain Representation. Returns the validated instance under the
same rules as `create`. Raises `ValidationError` when a rule is broken.

```python
from model import Broker, deserialize

broker = deserialize(
    Broker, {"id": None, "name": "FxPro", "user_id": 1, "is_active": True, "description": None}
)
print(broker)
```

### Reading a declaration

The vocabulary types let a consumer act on a declaration without guessing from names:

```python
from model import AtRest, User, describe

credentials = [f.name for f in describe(User).fields if f.credential is AtRest.HASH]
activation = [f.name for f in describe(User).fields if f.activation]
print(credentials, activation)
```

### Domain Definitions

Every definition is persistent, has a generated identity `id`, and declares `is_active` as its
activation Field. Where the Target states no length bound for text, none is declared.

### User

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `name` | string | unique |
| `username` | string | unique |
| `password` | string | credential, at rest: hash |
| `api_key` | string | credential, at rest: hash |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

```python
from model import User

record = User(
    name="Admin",
    username="admin",
    password="<placeholder>",
    api_key="<placeholder>",
    description=None,
)
print(record.serialize())
```
### TradingPlatform

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `name` | string | unique |
| `code` | string | required |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

```python
from model import TradingPlatform

record = TradingPlatform(name="MetaTrader 5", code="metatrader_5", description=None)
print(record.serialize())
```
### Instance

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `user_id` | integer | required |
| `trading_platform_id` | integer | required |
| `name` | string | required |
| `ip` | string | optional (supply `None`) |
| `username` | string | optional (supply `None`) |
| `password` | string | credential, at rest: encrypted; optional (supply `None`) |
| `api_key` | string | credential, at rest: encrypted; optional (supply `None`) |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `user` — `user_id` refers to `User.id`
- `trading_platform` — `trading_platform_id` refers to `TradingPlatform.id`

Unique together: (`user_id`, `name`)

```python
from model import Instance

record = Instance(
    user_id=1,
    trading_platform_id=1,
    name="MetaTrader",
    ip="127.0.0.1",
    username="test",
    password="<placeholder>",
    api_key="<placeholder>",
    description=None,
)
print(record.serialize())
```
### Currency

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `user_id` | integer | required |
| `code` | string | length ≤ 3 |
| `symbol` | string | optional (supply `None`) |
| `country` | string | optional (supply `None`) |
| `decimal_digits` | integer | default `2` |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `user` — `user_id` refers to `User.id`

Unique together: (`user_id`, `code`)

```python
from model import Currency

record = Currency(user_id=1, code="USD", symbol="$", country="United States", description=None)
print(record.serialize())
```
### Broker

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `name` | string | required |
| `user_id` | integer | required |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `user` — `user_id` refers to `User.id`

Unique together: (`user_id`, `name`)

```python
from model import Broker

record = Broker(name="FxPro", user_id=1, description=None)
print(record.serialize())
```
### Asset

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `broker_id` | integer | required |
| `symbol` | string | required |
| `category` | string | required |
| `point_size` | float | default `0.0` |
| `digits` | integer | default `0` |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `broker` — `broker_id` refers to `Broker.id`

Unique together: (`broker_id`, `symbol`)

```python
from model import Asset

record = Asset(
    broker_id=1,
    symbol="EUR/USD",
    category="Currency",
    point_size=0.0001,
    digits=5,
    description=None,
)
print(record.serialize())
```
### AccountGroup

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `user_id` | integer | required |
| `name` | string | required |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `user` — `user_id` refers to `User.id`

Unique together: (`user_id`, `name`)

```python
from model import AccountGroup

record = AccountGroup(user_id=1, name="Default", description=None)
print(record.serialize())
```
### Account

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `name` | string | unique |
| `group_id` | integer | required |
| `broker_id` | integer | required |
| `instance_id` | integer | required |
| `base_currency_id` | integer | required |
| `username` | string | required |
| `password` | string | credential, at rest: encrypted |
| `leverage` | integer | required |
| `balance` | decimal | default `Decimal('0')` |
| `account_type` | string | required |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `group` — `group_id` refers to `AccountGroup.id`
- `broker` — `broker_id` refers to `Broker.id`
- `instance` — `instance_id` refers to `Instance.id`
- `base_currency` — `base_currency_id` refers to `Currency.id`

Unique together: (`group_id`, `broker_id`, `instance_id`)

```python
from model import Account

record = Account(
    name="Acc-1",
    group_id=1,
    broker_id=1,
    instance_id=1,
    base_currency_id=1,
    username="test",
    password="<placeholder>",
    leverage=100,
    account_type="CFD",
    description=None,
)
print(record.serialize())
```
### TrailingGroup

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `user_id` | integer | required |
| `name` | string | required |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `user` — `user_id` refers to `User.id`

Unique together: (`user_id`, `name`)

```python
from model import TrailingGroup

record = TrailingGroup(user_id=1, name="Default", description=None)
print(record.serialize())
```
### TrailingRule

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `name` | string | unique |
| `trailing_group_id` | integer | required |
| `trigger_percentage` | decimal | required |
| `take_profit_adjustment` | decimal | optional (supply `None`) |
| `stop_loss_adjustment` | decimal | optional (supply `None`) |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `trailing_group` — `trailing_group_id` refers to `TrailingGroup.id`

Unique together: (`trailing_group_id`, `trigger_percentage`)

```python
from model import TrailingRule

record = TrailingRule(
    name="Move to break-even",
    trailing_group_id=1,
    trigger_percentage="50",
    take_profit_adjustment=None,
    stop_loss_adjustment="0",
    description=None,
)
print(record.serialize())
```
### PartialGroup

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `user_id` | integer | required |
| `name` | string | required |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `user` — `user_id` refers to `User.id`

Unique together: (`user_id`, `name`)

```python
from model import PartialGroup

record = PartialGroup(user_id=1, name="Default", description=None)
print(record.serialize())
```
### PartialRule

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `name` | string | unique |
| `partial_group_id` | integer | required |
| `profit_percentage` | decimal | required |
| `close_percentage` | decimal | required |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `partial_group` — `partial_group_id` refers to `PartialGroup.id`

Unique together: (`partial_group_id`, `profit_percentage`)

```python
from model import PartialRule

record = PartialRule(
    name="Half at 50%",
    partial_group_id=1,
    profit_percentage="50",
    close_percentage="50",
    description=None,
)
print(record.serialize())
```
### ActionGroup

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `user_id` | integer | required |
| `name` | string | required |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `user` — `user_id` refers to `User.id`

Unique together: (`user_id`, `name`)

```python
from model import ActionGroup

record = ActionGroup(user_id=1, name="Default", description=None)
print(record.serialize())
```
### Action

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `name` | string | required |
| `action_group_id` | integer | required |
| `asset_id` | integer | required |
| `account_id` | integer | required |
| `partial_group_id` | integer | required |
| `trailing_group_id` | integer | required |
| `risk_by_reward` | decimal | required |
| `take_profit` | decimal | required |
| `stop_loss` | decimal | required |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `action_group` — `action_group_id` refers to `ActionGroup.id`
- `asset` — `asset_id` refers to `Asset.id`
- `account` — `account_id` refers to `Account.id`
- `partial_group` — `partial_group_id` refers to `PartialGroup.id`
- `trailing_group` — `trailing_group_id` refers to `TrailingGroup.id`

Unique together: (`action_group_id`, `name`)

```python
from model import Action

record = Action(
    name="Default",
    action_group_id=1,
    asset_id=1,
    account_id=1,
    partial_group_id=1,
    trailing_group_id=1,
    risk_by_reward="1",
    take_profit="1",
    stop_loss="1",
    description=None,
)
print(record.serialize())
```
### Position

| Field | Type | Terms |
|---|---|---|
| `id` | integer | identity; generated — no value until produced |
| `user_id` | integer | required |
| `name` | string | unique |
| `trading_platform_id` | integer | required |
| `broker_id` | integer | required |
| `account_id` | integer | required |
| `trailing_group_id` | integer | required |
| `partial_group_id` | integer | required |
| `action_group_id` | integer | required |
| `action_id` | integer | required |
| `date` | datetime | required |
| `volume` | decimal | required |
| `profit` | decimal | default `Decimal('0')` |
| `is_executed` | boolean | default `False` |
| `order_type` | string | required |
| `base_tp` | decimal | required |
| `base_sl` | decimal | required |
| `real_tp` | decimal | required |
| `real_sl` | decimal | required |
| `is_active` | boolean | activation; default `True` |
| `description` | string | optional (supply `None`) |

Relationships (each: one, required):
- `user` — `user_id` refers to `User.id`
- `trading_platform` — `trading_platform_id` refers to `TradingPlatform.id`
- `broker` — `broker_id` refers to `Broker.id`
- `account` — `account_id` refers to `Account.id`
- `trailing_group` — `trailing_group_id` refers to `TrailingGroup.id`
- `partial_group` — `partial_group_id` refers to `PartialGroup.id`
- `action_group` — `action_group_id` refers to `ActionGroup.id`
- `action` — `action_id` refers to `Action.id`

```python
from datetime import datetime, timezone

from model import Position

record = Position(
    user_id=1,
    name="P-1",
    trading_platform_id=1,
    broker_id=1,
    account_id=1,
    trailing_group_id=1,
    partial_group_id=1,
    action_group_id=1,
    action_id=1,
    date=datetime(2026, 1, 1, 9, 30, tzinfo=timezone.utc),
    volume="0.10",
    order_type="market",
    base_tp="1.1000",
    base_sl="1.0900",
    real_tp="1.1000",
    real_sl="1.0900",
    description=None,
)
print(record.serialize())
```
## Setup

Requires Python 3.14 or newer and [uv](https://docs.astral.sh/uv/).

```bash
cd model
uv sync
```

To use Model from another package, depend on it by path (no registry publication is configured):

```bash
uv add --editable ../model
```

## Run

Model is a library: there is no process to start. Import from `model` and call the Operations
above.

## Verify

```bash
uv run python -c "import model; print(model.describe(model.User).persistence)"   # persistent
uv run ruff format --check
uv run ruff check
uv run pyright
```

The Model carries no test suite of its own; these checks and the examples in this file are its
verification.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Input should be a valid integer` for `"1"` | Types are strict | Pass an `int`. |
| `Input should be a valid boolean` | Text or a number given for a boolean | Pass `True` or `False`. |
| `an exact decimal must not be supplied as a floating point number` | A `float` was given for a decimal | Pass text or an integer, e.g. `"0.10"`. |
| `an absolute instant must carry timezone information` | A naive `datetime` | Add `tzinfo`, e.g. `timezone.utc`. |
| `Field required` for an optional Field | Optional Fields have no default | Supply `None` explicitly. |
| `Extra inputs are not permitted` | A name the definition does not declare | Remove it, or check the spelling with `describe`. |
| `ModuleNotFoundError: model` | The package is not installed in this environment | Run `uv sync`, or `uv add --editable ../model`. |

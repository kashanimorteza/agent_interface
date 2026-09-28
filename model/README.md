# Model

## Overview

Model defines the Trading Assistant's data-model Entities as a small, reusable Python library. Each Entity is one flat, self-contained definition of a domain concept, and other Components use Model through its published surface.

```python
from model.interface import Currency

usd = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(usd.decimal_digits)
print(usd.to_json())
```

```text
2
{"user_id": 1, "code": "USD", "symbol": "$", "country": "United States", "id": null, "decimal_digits": 2, "is_active": true, "description": null}
```

## Interface

Every Entity below is published through the standard entry point. Each Entity has an `id` Identity and Primary Key.

### Account

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `name` | string | no | none | unique |
| `group_id` | integer | no | none | references AccountGroup |
| `broker_id` | integer | no | none | references Broker |
| `instance_id` | integer | no | none | references Instance |
| `base_currency_id` | integer | no | none | references Currency |
| `username` | string | no | none |  |
| `password` | string | no | none | sensitivity marker `password` |
| `leverage` | integer | no | none |  |
| `balance` | decimal | no | `Decimal('0')` |  |
| `account_type` | string | no | none |  |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

Unique together: (`group_id`, `broker_id`, `instance_id`).

### AccountGroup

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `user_id` | integer | no | none | references User |
| `name` | string | no | none |  |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

Unique together: (`user_id`, `name`).

### Action

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `name` | string | no | none |  |
| `action_group_id` | integer | no | none | references ActionGroup |
| `asset_id` | integer | no | none | references Asset |
| `account_id` | integer | no | none | references Account |
| `partial_group_id` | integer | no | none | references PartialGroup |
| `trailing_group_id` | integer | no | none | references TrailingGroup |
| `risk_by_reward` | decimal | no | none |  |
| `take_profit` | decimal | no | none |  |
| `stop_loss` | decimal | no | none |  |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

Unique together: (`action_group_id`, `name`).

### ActionGroup

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `user_id` | integer | no | none | references User |
| `name` | string | no | none |  |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

Unique together: (`user_id`, `name`).

### Asset

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `broker_id` | integer | no | none | references Broker |
| `symbol` | string | no | none |  |
| `category` | string | no | none |  |
| `point_size` | float | no | `0.0` |  |
| `digits` | integer | no | `0` |  |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

Unique together: (`broker_id`, `symbol`).

### Broker

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `name` | string | no | none |  |
| `user_id` | integer | no | none | references User |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

Unique together: (`user_id`, `name`).

### Currency

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `user_id` | integer | no | none | references User |
| `code` | string | no | none | length 3 |
| `symbol` | string | yes | none |  |
| `country` | string | yes | none |  |
| `decimal_digits` | integer | no | `2` |  |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

Unique together: (`user_id`, `code`).

### Instance

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `user_id` | integer | no | none | references User |
| `trading_platform_id` | integer | no | none | references TradingPlatform |
| `name` | string | no | none |  |
| `ip` | string | yes | none |  |
| `username` | string | yes | none |  |
| `password` | string | yes | none | sensitivity marker `password` |
| `api_key` | string | yes | none | sensitivity marker `sensitive` |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

Unique together: (`user_id`, `name`).

### PartialGroup

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `user_id` | integer | no | none | references User |
| `name` | string | no | none |  |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

Unique together: (`user_id`, `name`).

### PartialRule

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `name` | string | no | none | unique |
| `partial_group_id` | integer | no | none | references PartialGroup |
| `profit_percentage` | decimal | no | none |  |
| `close_percentage` | decimal | no | none |  |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

Unique together: (`partial_group_id`, `profit_percentage`).

### Position

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `user_id` | integer | no | none | references User |
| `name` | string | no | none | unique |
| `trading_platform_id` | integer | no | none | references TradingPlatform |
| `broker_id` | integer | no | none | references Broker |
| `account_id` | integer | no | none | references Account |
| `trailing_group_id` | integer | no | none | references TrailingGroup |
| `partial_group_id` | integer | no | none | references PartialGroup |
| `action_group_id` | integer | no | none | references ActionGroup |
| `action_id` | integer | no | none | references Action |
| `date` | datetime | no | none |  |
| `volume` | decimal | no | none |  |
| `profit` | decimal | no | `Decimal('0')` |  |
| `is_executed` | boolean | no | `False` |  |
| `order_type` | string | no | none |  |
| `base_tp` | decimal | no | none |  |
| `base_sl` | decimal | no | none |  |
| `real_tp` | decimal | no | none |  |
| `real_sl` | decimal | no | none |  |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

### TradingPlatform

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `name` | string | no | none | unique |
| `code` | string | no | none |  |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

### TrailingGroup

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `user_id` | integer | no | none | references User |
| `name` | string | no | none |  |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

Unique together: (`user_id`, `name`).

### TrailingRule

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `name` | string | no | none | unique |
| `trailing_group_id` | integer | no | none | references TrailingGroup |
| `trigger_percentage` | decimal | no | none |  |
| `take_profit_adjustment` | decimal | yes | none |  |
| `stop_loss_adjustment` | decimal | yes | none |  |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

Unique together: (`trailing_group_id`, `trigger_percentage`).

### User

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no | auto increment | primary key |
| `name` | string | no | none | unique |
| `username` | string | no | none | unique |
| `password` | string | no | none | sensitivity marker `password` |
| `api_key` | string | no | none | sensitivity marker `sensitive` |
| `is_active` | boolean | no | `True` |  |
| `description` | string | yes | none |  |

## Foundation

Foundation supplies the shared behaviour every Entity inherits: converting an Entity to JSON and constructing an Entity from JSON. It adds no Fields or rules of its own.

### Entity to JSON

```python
from model.interface import Broker

broker = Broker(name="FxPro", user_id=1)
print(broker.to_json())
```

```text
{"name": "FxPro", "user_id": 1, "id": null, "is_active": true, "description": null}
```

### JSON to Entity

```python
from model.interface import Broker

broker = Broker.from_json('{"name": "FxPro", "user_id": 1}')
print(broker.name, broker.is_active)
```

```text
FxPro True
```

### Complete example

```python
from model.interface import Broker

original = Broker(name="FxPro", user_id=1)
document = original.to_json()
restored = Broker.from_json(document)
print(document)
print(restored.model_dump() == original.model_dump())
```

```text
{"name": "FxPro", "user_id": 1, "id": null, "is_active": true, "description": null}
True
```

## Setup

Model needs Python 3.14 or newer and is managed with [uv](https://docs.astral.sh/uv/).

To use Model from another project, add it as a dependency from the directory that holds the Model Component:

```bash
uv add ../model
```

To work on Model itself, install its environment from the Model Component root:

```bash
uv sync
```

Confirm the setup by importing a published Entity:

```bash
uv run python -c "from model.interface import User; print(User.__name__)"
```

```text
User
```

## Use

Import Entities from the standard entry point and create them with keyword arguments. Omitted Fields take their declared defaults, so an Entity needs only its required Fields.

Every Entity publishes its meaning through a `declaration`: its Identity and Primary Key, Fields, References, and sensitivity markers.

```python
from model.interface import Account

declaration = Account.declaration
print(declaration.entity, declaration.primary_key)
print([reference.entity for reference in declaration.references])
print(declaration.get_field("password").sensitivity)
```

```text
Account id
['AccountGroup', 'Broker', 'Instance', 'Currency']
password
```

Creating an Entity directly does not check its input. When the data comes from outside, construct it with `from_json`, which validates required Fields and value types:

```python
from pydantic import ValidationError

from model.interface import Broker

try:
    Broker.from_json('{"user_id": 1}')
except ValidationError:
    print("rejected: name is required")
```

```text
rejected: name is required
```

Keep in mind:

- A Reference holds another Entity's `id`. Entities never contain one another.
- A sensitivity marker only labels a Field. Model does not hash, encrypt, or otherwise handle its value; storage and protection belong to the Component that stores it.
- Model holds no records and performs no storage, transport, or workflow.

## Troubleshooting

### `ModuleNotFoundError: No module named 'model'`

The interpreter you ran is not the one Model was installed into. Add Model to the project as described in Setup, then run your code through the project's environment:

```bash
uv run python your_script.py
```

### `NoReferencedTableError` when creating tables

```text
sqlalchemy.exc.NoReferencedTableError: Foreign key associated with column 'instance.trading_platform_id' could not find table 'tradingplatform' ...
```

An Entity's References point at other Entities, and their tables must be known before the schema is created. This happens when only some Entity units were imported. Import the standard entry point first, which registers every Entity:

```python
from sqlmodel import SQLModel, create_engine

import model.interface

SQLModel.metadata.create_all(create_engine("sqlite://"))
print("created", len(SQLModel.metadata.tables), "tables")
```

```text
created 15 tables
```

### `ValidationError` from `from_json`

The JSON is missing a required Field or holds a value of the wrong type. Compare it with the Entity's Fields table in the Interface section and supply every Field marked as not nullable and without a default.

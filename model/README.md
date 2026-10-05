# Model

Model is the reusable data library of the Trading Assistant. It defines the application's data as flat, technology-independent Entities, publishes every Entity by name and as one ordered collection, exposes each Entity's complete meaning as a Declaration, and converts every Entity to and from JSON text without loss.

## Overview

Import an Entity from the Interface, create an instance, and convert it to JSON text:

```python
from model.interface import User

user = User(name="Example", username="example", password="example-password", api_key="example-key")
print(user.to_json())
```

A field that is not supplied takes its declared default. A value that is not valid is rejected instead of being corrected. An identifier that the storage layer assigns stays pending (`None`) until it is assigned.

## Interface

The Interface publishes exactly two things, and nothing else:

- **Entity Exports** — one explicit named export for every Entity, each being the actual Entity class.
- **Entity Collection** — `entities`, one immutable tuple holding every actual Entity in the order of the list below.

A consumer that works with one Entity imports it by name:

```python
from model.interface import Currency

currency = Currency(user_id=1, code="USD")
```

A consumer that works with every Entity enumerates the collection:

```python
from model.interface import entities

for entity in entities:
    print(entity.declaration.name)
```

Loading the Interface creates no instance, data, connection, file, or process.

### Entity reference

Every Entity, in Target order:

#### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `name` | string | no | none | none | The user's display name. |
| `username` | string | no | none | none | The username used to identify the user. |
| `password` | string | no | none | none | The password credential used by the user. |
| `api_key` | string | no | none | none | The API key assigned to the user. |
| `is_active` | boolean | no | true | none | Indicates whether the user is active. |
| `description` | string | yes | none | none | Describes the user. |

**Entity Metadata**

- Primary Key: `id`
- Relations: none
- Uniqueness Constraints: (`name`); (`username`)
- Indexes: none

#### Trading Platform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `name` | string | no | none | none | The platform's display name. |
| `code` | string | no | none | none | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | boolean | no | true | none | Indicates whether the platform is active. |
| `description` | string | yes | none | none | Describes the platform. |

**Entity Metadata**

- Primary Key: `id`
- Relations: none
- Uniqueness Constraints: (`name`)
- Indexes: none

#### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `user_id` | integer | no | none | none | Identifies the user who owns this instance. |
| `trading_platform_id` | integer | no | none | none | Identifies the trading platform used by this instance. |
| `name` | string | no | none | none | The instance's display name. |
| `ip` | string | yes | none | none | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | string | yes | none | none | Defines the technical username used to establish the Instance connection when required. |
| `password` | string | yes | none | none | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | string | yes | none | none | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | no | true | none | Indicates whether the instance is active. |
| `description` | string | yes | none | none | Describes the instance. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `user_id` → User.`id`; `trading_platform_id` → Trading Platform.`id`
- Uniqueness Constraints: (`user_id`, `name`)
- Indexes: none

#### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `user_id` | integer | no | none | none | Identifies the user who owns this currency. |
| `code` | string | no | none | size 3 | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | string | yes | none | none | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | string | yes | none | none | Identifies the country or region associated with the currency. |
| `decimal_digits` | integer | no | 2 | none | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | no | true | none | Indicates whether the currency is active. |
| `description` | string | yes | none | none | Describes the currency. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `user_id` → User.`id`
- Uniqueness Constraints: (`user_id`, `code`)
- Indexes: none

#### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `name` | string | no | none | none | The broker's display name. |
| `user_id` | integer | no | none | none | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | no | true | none | Indicates whether the broker is active. |
| `description` | string | yes | none | none | Describes the broker. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `user_id` → User.`id`
- Uniqueness Constraints: (`user_id`, `name`)
- Indexes: none

#### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `broker_id` | integer | no | none | none | Identifies the broker that provides this asset. |
| `symbol` | string | no | none | none | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | string | no | none | none | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | float | no | 0.0 | none | Stores the size of one point for the asset. |
| `digits` | integer | no | 0 | none | Stores the number of decimal digits used for the asset's price. |
| `is_active` | boolean | no | true | none | Indicates whether the asset is active. |
| `description` | string | yes | none | none | Describes the asset. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `broker_id` → Broker.`id`
- Uniqueness Constraints: (`broker_id`, `symbol`)
- Indexes: none

#### Account Group

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `user_id` | integer | no | none | none | Identifies the user who owns the account group. |
| `name` | string | no | none | none | The account group's display name. |
| `is_active` | boolean | no | true | none | Indicates whether the account group is active. |
| `description` | string | yes | none | none | Describes the account group. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `user_id` → User.`id`
- Uniqueness Constraints: (`user_id`, `name`)
- Indexes: none

#### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `name` | string | no | none | none | The account's display name. |
| `group_id` | integer | no | none | none | Identifies the account group that contains the account. |
| `broker_id` | integer | no | none | none | Identifies the broker that owns the account. |
| `instance_id` | integer | no | none | none | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | no | none | none | Identifies the base currency used by the account. |
| `username` | string | no | none | none | The username identifier used to access the trading account. |
| `password` | string | no | none | none | The credential used to access the trading account. |
| `leverage` | integer | no | none | none | Defines the account's leverage multiplier. |
| `balance` | decimal | no | 0 | none | Stores the account's current balance. |
| `account_type` | string | no | none | none | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | boolean | no | true | none | Indicates whether the account is active. |
| `description` | string | yes | none | none | Describes the account. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `group_id` → Account Group.`id`; `broker_id` → Broker.`id`; `instance_id` → Instance.`id`; `base_currency_id` → Currency.`id`
- Uniqueness Constraints: (`name`); (`group_id`, `broker_id`, `instance_id`)
- Indexes: none

#### Trailing Group

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `user_id` | integer | no | none | none | Identifies the user who owns the trailing group. |
| `name` | string | no | none | none | The trailing group's display name. |
| `is_active` | boolean | no | true | none | Indicates whether the trailing group is active. |
| `description` | string | yes | none | none | Describes the trailing group. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `user_id` → User.`id`
- Uniqueness Constraints: (`user_id`, `name`)
- Indexes: none

#### Trailing Rule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `name` | string | no | none | none | The trailing rule's display name. |
| `trailing_group_id` | integer | no | none | none | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | decimal | no | none | none | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | decimal | yes | none | none | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | decimal | yes | none | none | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | boolean | no | true | none | Indicates whether the trailing rule is active. |
| `description` | string | yes | none | none | Describes the trailing rule. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `trailing_group_id` → Trailing Group.`id`
- Uniqueness Constraints: (`name`); (`trailing_group_id`, `trigger_percentage`)
- Indexes: none

#### Partial Group

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `user_id` | integer | no | none | none | Identifies the user who owns the partial group. |
| `name` | string | no | none | none | The partial group's display name. |
| `is_active` | boolean | no | true | none | Indicates whether the partial group is active. |
| `description` | string | yes | none | none | Describes the partial group. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `user_id` → User.`id`
- Uniqueness Constraints: (`user_id`, `name`)
- Indexes: none

#### Partial Rule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `name` | string | no | none | none | The partial rule's display name. |
| `partial_group_id` | integer | no | none | none | Identifies the partial group that contains the rule. |
| `profit_percentage` | decimal | no | none | none | Defines the profit percentage that activates the rule. |
| `close_percentage` | decimal | no | none | none | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | boolean | no | true | none | Indicates whether the partial rule is active. |
| `description` | string | yes | none | none | Describes the partial rule. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `partial_group_id` → Partial Group.`id`
- Uniqueness Constraints: (`name`); (`partial_group_id`, `profit_percentage`)
- Indexes: none

#### Action Group

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `user_id` | integer | no | none | none | Identifies the user who owns the action group. |
| `name` | string | no | none | none | The action group's display name. |
| `is_active` | boolean | no | true | none | Indicates whether the action group is active. |
| `description` | string | yes | none | none | Describes the action group. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `user_id` → User.`id`
- Uniqueness Constraints: (`user_id`, `name`)
- Indexes: none

#### Action

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `name` | string | no | none | none | The action's display name. |
| `action_group_id` | integer | no | none | none | Identifies the action group that contains the action. |
| `asset_id` | integer | no | none | none | Identifies the asset traded by the action. |
| `account_id` | integer | no | none | none | Identifies the account used to execute the action. |
| `partial_group_id` | integer | no | none | none | Identifies the Partial Group used by the action. |
| `trailing_group_id` | integer | no | none | none | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | decimal | no | none | none | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | decimal | no | none | none | Defines the Take Profit value used by the action. |
| `stop_loss` | decimal | no | none | none | Defines the Stop Loss value used by the action. |
| `is_active` | boolean | no | true | none | Indicates whether the action is active. |
| `description` | string | yes | none | none | Describes the action. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `action_group_id` → Action Group.`id`; `asset_id` → Asset.`id`; `account_id` → Account.`id`; `partial_group_id` → Partial Group.`id`; `trailing_group_id` → Trailing Group.`id`
- Uniqueness Constraints: (`action_group_id`, `name`)
- Indexes: none

#### Position

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | none | immutable, generated (auto_increment) |  |
| `user_id` | integer | no | none | none | Identifies the user who owns the position. |
| `name` | string | no | none | none | The position's display name. |
| `trading_platform_id` | integer | no | none | none | Identifies the trading platform used to execute the position. |
| `broker_id` | integer | no | none | none | Identifies the broker through which the position is executed. |
| `account_id` | integer | no | none | none | Identifies the trading account used for the position. |
| `trailing_group_id` | integer | no | none | none | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | integer | no | none | none | Identifies the Partial Group applied to the position. |
| `action_group_id` | integer | no | none | none | Identifies the Action Group associated with the position. |
| `action_id` | integer | no | none | none | Identifies the action from which the position is created. |
| `date` | datetime | no | none | none | Stores the position's date and time. |
| `volume` | decimal | no | none | none | Stores the position's trading volume. |
| `profit` | decimal | no | 0 | none | Stores the position's current profit or loss. |
| `is_executed` | boolean | no | false | none | Indicates whether the position has been executed. |
| `order_type` | string | no | none | none | Stores the position's order type. |
| `base_tp` | decimal | no | none | none | Stores the position's initial Take Profit value. |
| `base_sl` | decimal | no | none | none | Stores the position's initial Stop Loss value. |
| `real_tp` | decimal | no | none | none | Stores the position's current Take Profit value. |
| `real_sl` | decimal | no | none | none | Stores the position's current Stop Loss value. |
| `is_active` | boolean | no | true | none | Indicates whether the position is active. |
| `description` | string | yes | none | none | Describes the position. |

**Entity Metadata**

- Primary Key: `id`
- Relations: `user_id` → User.`id`; `trading_platform_id` → Trading Platform.`id`; `broker_id` → Broker.`id`; `account_id` → Account.`id`; `trailing_group_id` → Trailing Group.`id`; `partial_group_id` → Partial Group.`id`; `action_group_id` → Action Group.`id`; `action_id` → Action.`id`
- Uniqueness Constraints: (`name`)
- Indexes: none

## Declaration

Every Entity exposes its own complete, immutable Declaration through its `declaration` attribute. The Declaration holds the Entity's name, description, ordered Fields, Primary Key, Relations, Uniqueness Constraints, and Indexes; each Field holds its name, description, Type, nullability, whether a default was declared and its value, sensitivity, immutability, constraints, and value generation.

```python
from model.interface import Instance

declaration = Instance.declaration
print(declaration.name, declaration.description)

for field in declaration.fields:
    print(field.name, field.type, field.nullable, field.has_default, field.default, field.immutable, field.value_generation)

print(declaration.primary_key)
for relation in declaration.relations:
    print(relation.local_field, relation.target_entity, relation.target_field)
print(declaration.unique_constraints)
print(declaration.indexes)
```

`has_default` separates an absent default from an explicit `null` default. A Declaration holds meaning only: no storage, transport, or workflow information.

## Foundation

Every Entity converts to a JSON Object and back through two capabilities. A JSON Object is JSON text with one object at its root whose keys are exactly the Entity's Field names, in Declaration order. Decimal values are written as strings so that they keep their exact value, and datetime values are written as ISO 8601 strings with an offset.

`to_json` converts an Entity to JSON text:

```python
from decimal import Decimal

from model.interface import TrailingRule

rule = TrailingRule(name="Example", trailing_group_id=1, trigger_percentage=Decimal("50.5"))
text = rule.to_json()
print(text)
```

`from_json` builds an Entity from JSON text. It rejects text that is not valid JSON, has no object at its root, names an unknown key, omits a required value, or carries a value of the wrong Type:

```python
from model.interface import TrailingRule

text = '{"id":null,"name":"Example","trailing_group_id":1,"trigger_percentage":"50.5","take_profit_adjustment":null,"stop_loss_adjustment":null,"is_active":true,"description":null}'
restored = TrailingRule.from_json(text)
print(restored.trigger_percentage)
```

A complete round trip, from Entity to JSON text and back to an equal Entity:

```python
from decimal import Decimal

from model.interface import TrailingRule

original = TrailingRule(name="Example", trailing_group_id=1, trigger_percentage=Decimal("50.5"))
restored = TrailingRule.from_json(original.to_json())

assert restored.to_json() == original.to_json()
assert restored.trigger_percentage == Decimal("50.5")
assert restored.take_profit_adjustment is None
```


## Setup

Model requires Python 3.14 and [uv](https://docs.astral.sh/uv/). All dependencies are pinned in `pyproject.toml` and `uv.lock`.

1. Open a terminal in the Component root, the directory that holds `pyproject.toml`.
2. Create the isolated environment and install the pinned dependencies:

   ```bash
   uv sync
   ```

3. Confirm that the Interface loads:

   ```bash
   uv run python -c "import model.interface"
   ```

To use Model from another project, add the Component root as a dependency of that project:

```bash
uv add ../model
```

The development tools (`ruff`, `pyright`) are installed by `uv sync` as development dependencies:

```bash
uv run ruff check model
uv run ruff format --check model
uv run pyright
```

## Use

Use Model through the Entity Exports and the Entity Collection only.

Create an Entity from valid values. Omitted Fields take their declared defaults, and an identifier assigned by storage stays pending:

```python
from model.interface import Broker

broker = Broker(name="Example", user_id=1)
print(broker.id, broker.is_active)
```

Change a mutable Field by assignment. A value that is not valid is rejected and the earlier value is kept; `id` cannot be assigned:

```python
from model.interface import Broker

broker = Broker(name="Example", user_id=1)
broker.name = "Renamed"
```

Work with every Entity without knowing their names:

```python
from model.interface import entities

for entity in entities:
    declaration = entity.declaration
    print(declaration.name, len(declaration.fields), declaration.primary_key)
```

Read an Entity's meaning from its Declaration, and convert it to JSON text and back:

```python
from model.interface import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States")
assert Currency.from_json(currency.to_json()).to_json() == currency.to_json()
print(Currency.declaration.unique_constraints)
```

Values keep their declared Types and are never converted: decimal Fields take `decimal.Decimal`, float Fields take `float`, datetime Fields take timezone-aware `datetime` values, and no Field accepts an unknown name.

## Verify

Run the following from the Component root. Every assertion states one observation about the Model; the script ends silently when all of them hold.

```python
import os
from decimal import Decimal

TARGET_ORDER = [
    "User", "Trading Platform", "Instance", "Currency", "Broker", "Asset", "Account Group", "Account",
    "Trailing Group", "Trailing Rule", "Partial Group", "Partial Rule", "Action Group", "Action", "Position",
]


def files():
    return {
        os.path.join(root, name)
        for root, _, names in os.walk(".")
        for name in names
        if "__pycache__" not in root and ".venv" not in root
    }


# Loading the Interface has no side effect.
before = files()
import model.interface as interface

assert files() == before

# The Interface shape: the Entity Exports plus the Entity Collection, nothing else.
public = [name for name in vars(interface) if not name.startswith("_")]
assert "entities" in public
exports = [name for name in public if name != "entities"]
assert len(exports) == len(TARGET_ORDER)

# Entity Collection: exact membership and order, corresponding to the exports.
collection = interface.entities
assert isinstance(collection, tuple)
assert [entity.declaration.name for entity in collection] == TARGET_ORDER
assert sorted(entity.__name__ for entity in collection) == sorted(exports)

# Actual references: each export and each member is the Entity's own class and Declaration.
for entity in collection:
    assert getattr(interface, entity.__name__) is entity
    assert entity.declaration is entity.__dict__["declaration"]
    assert entity.declaration.primary_key == "id"
    assert entity.declaration.fields[0].name == "id"

# Representative construction, Declaration access, and immutability.
user = interface.User(name="Example", username="example", password="example-password", api_key="example-key")
assert user.id is None and user.is_active is True
assert [field.name for field in interface.User.declaration.fields][:2] == ["id", "name"]
try:
    user.id = 1
except ValueError:
    pass
else:
    raise AssertionError("id must not be assignable")
try:
    interface.User(name=1, username="example", password="example-password", api_key="example-key")
except Exception:
    pass
else:
    raise AssertionError("a wrong Type must be rejected")

# A lossless round trip through JSON text, including an exact decimal.
rule = interface.TrailingRule(name="Example", trailing_group_id=1, trigger_percentage=Decimal("0.10000000000000000001"))
restored = interface.TrailingRule.from_json(rule.to_json())
assert restored.trigger_percentage == Decimal("0.10000000000000000001")
assert restored.to_json() == rule.to_json()
```

## Troubleshooting

- **`ValidationError` when creating an Entity or assigning a Field.** The value was rejected rather than corrected. The message names the Field and the rule it broke, never the value. Check the Field's Type in the Entity reference: decimal Fields need `decimal.Decimal` (not `int` or `float`), float Fields need `float` (not `int`), datetime Fields need a timezone-aware `datetime`, and a Field marked not nullable cannot be `None`.
- **`ValidationError` naming an extra input.** The Entity has no Field of that name. Entities accept only their declared Fields.
- **`ValueError: Field 'id' is generated and cannot be supplied`.** `id` is assigned by storage. Omit it (or pass `None`) when creating an Entity; `id` cannot be assigned afterwards.
- **`ValueError: Field '…' cannot be assigned`.** The Field is immutable or generated. Only mutable Fields accept assignment.
- **`ValueError: Text is not valid JSON` or `JSON text must have one object at its root`.** `from_json` accepts only JSON text whose root is one object. Decimal values must be strings, and datetime values must be ISO 8601 strings with an offset.
- **`ValueError: Unknown Type '…'`.** A Declaration named a Type that Model does not support. Model stops instead of guessing; use one of the supported Types listed in the message.
- **Setup fails because the Python version is not supported.** Model requires Python 3.14. Install it, or let `uv` provide it, then run `uv sync` again.
- **`ModuleNotFoundError: No module named 'model'`.** Run the command from the Component root with `uv run`, so that the Component's environment is used.

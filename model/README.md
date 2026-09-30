# Model

Model is the reusable, storage-independent data library of the Trading Assistant. It defines flat Entities with their Fields and metadata and publishes each Entity's complete meaning as a Declaration. It owns no tables, queries, storage, transport, or behaviour.

```python
from model import User

user = User(name="Ada", username="ada", password="placeholder", api_key="placeholder")
print(user.username, user.is_active, user.id)
```

Output:

```text
ada True None
```

`id` stays `None` (pending) until the owner of the identity assigns it; `is_active` defaults to `true`.

## Interface

Every public Entity, once, in Target order. Each is published by both the package root and the standard entrypoint. Each Entity is flat and independent: cross-Entity meaning is recorded only as Relation metadata.

### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

Published as `User`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `name` | string | no | — | — | no | — | — | The user's display name. |
| `username` | string | no | — | — | no | — | — | The username used to identify the user. |
| `password` | string | no | — | password | no | — | — | The password credential used by the user. |
| `api_key` | string | no | — | sensitive | no | — | — | The API key assigned to the user. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the user is active. |
| `description` | string | yes | — | — | no | — | — | Describes the user. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** (`name`); (`username`)
- **Indexes:** none

### Trading Platform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

Published as `TradingPlatform`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `name` | string | no | — | — | no | — | — | The platform's display name. |
| `code` | string | no | — | — | no | — | — | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the platform is active. |
| `description` | string | yes | — | — | no | — | — | Describes the platform. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** (`name`)
- **Indexes:** none

### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

Published as `Instance`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `user_id` | integer | no | — | — | no | — | — | Identifies the user who owns this instance. |
| `trading_platform_id` | integer | no | — | — | no | — | — | Identifies the trading platform used by this instance. |
| `name` | string | no | — | — | no | — | — | The instance's display name. |
| `ip` | string | yes | — | — | no | — | — | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | string | yes | — | — | no | — | — | Defines the technical username used to establish the Instance connection when required. |
| `password` | string | yes | — | password | no | — | — | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | string | yes | — | sensitive | no | — | — | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the instance is active. |
| `description` | string | yes | — | — | no | — | — | Describes the instance. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`; `trading_platform_id` → Trading Platform.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

Published as `Currency`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `user_id` | integer | no | — | — | no | — | — | Identifies the user who owns this currency. |
| `code` | string | no | — | — | no | — | size 3 | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | string | yes | — | — | no | — | — | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | string | yes | — | — | no | — | — | Identifies the country or region associated with the currency. |
| `decimal_digits` | integer | no | `2` | — | no | — | — | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the currency is active. |
| `description` | string | yes | — | — | no | — | — | Describes the currency. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `code`)
- **Indexes:** none

### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

Published as `Broker`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `name` | string | no | — | — | no | — | — | The broker's display name. |
| `user_id` | integer | no | — | — | no | — | — | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the broker is active. |
| `description` | string | yes | — | — | no | — | — | Describes the broker. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

Published as `Asset`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `broker_id` | integer | no | — | — | no | — | — | Identifies the broker that provides this asset. |
| `symbol` | string | no | — | — | no | — | — | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | string | no | — | — | no | — | — | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | float | no | `0.0` | — | no | — | — | Stores the size of one point for the asset. |
| `digits` | integer | no | `0` | — | no | — | — | Stores the number of decimal digits used for the asset's price. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the asset is active. |
| `description` | string | yes | — | — | no | — | — | Describes the asset. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `broker_id` → Broker.`id`
- **Uniqueness Constraints:** (`broker_id`, `symbol`)
- **Indexes:** none

### Account Group

Defines an independent group for organizing trading accounts owned by one user.

Published as `AccountGroup`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `user_id` | integer | no | — | — | no | — | — | Identifies the user who owns the account group. |
| `name` | string | no | — | — | no | — | — | The account group's display name. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the account group is active. |
| `description` | string | yes | — | — | no | — | — | Describes the account group. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

Published as `Account`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `name` | string | no | — | — | no | — | — | The account's display name. |
| `group_id` | integer | no | — | — | no | — | — | Identifies the account group that contains the account. |
| `broker_id` | integer | no | — | — | no | — | — | Identifies the broker that owns the account. |
| `instance_id` | integer | no | — | — | no | — | — | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | no | — | — | no | — | — | Identifies the base currency used by the account. |
| `username` | string | no | — | — | no | — | — | The username identifier used to access the trading account. |
| `password` | string | no | — | password | no | — | — | The credential used to access the trading account. |
| `leverage` | integer | no | — | — | no | — | — | Defines the account's leverage multiplier. |
| `balance` | decimal | no | `0` | — | no | — | — | Stores the account's current balance. |
| `account_type` | string | no | — | — | no | — | — | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the account is active. |
| `description` | string | yes | — | — | no | — | — | Describes the account. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `group_id` → Account Group.`id`; `broker_id` → Broker.`id`; `instance_id` → Instance.`id`; `base_currency_id` → Currency.`id`
- **Uniqueness Constraints:** (`name`); (`group_id`, `broker_id`, `instance_id`)
- **Indexes:** none

### Trailing Group

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

Published as `TrailingGroup`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `user_id` | integer | no | — | — | no | — | — | Identifies the user who owns the trailing group. |
| `name` | string | no | — | — | no | — | — | The trailing group's display name. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the trailing group is active. |
| `description` | string | yes | — | — | no | — | — | Describes the trailing group. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Trailing Rule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

Published as `TrailingRule`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `name` | string | no | — | — | no | — | — | The trailing rule's display name. |
| `trailing_group_id` | integer | no | — | — | no | — | — | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | decimal | no | — | — | no | — | — | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | decimal | yes | — | — | no | — | — | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | decimal | yes | — | — | no | — | — | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the trailing rule is active. |
| `description` | string | yes | — | — | no | — | — | Describes the trailing rule. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `trailing_group_id` → Trailing Group.`id`
- **Uniqueness Constraints:** (`name`); (`trailing_group_id`, `trigger_percentage`)
- **Indexes:** none

### Partial Group

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

Published as `PartialGroup`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `user_id` | integer | no | — | — | no | — | — | Identifies the user who owns the partial group. |
| `name` | string | no | — | — | no | — | — | The partial group's display name. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the partial group is active. |
| `description` | string | yes | — | — | no | — | — | Describes the partial group. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Partial Rule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

Published as `PartialRule`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `name` | string | no | — | — | no | — | — | The partial rule's display name. |
| `partial_group_id` | integer | no | — | — | no | — | — | Identifies the partial group that contains the rule. |
| `profit_percentage` | decimal | no | — | — | no | — | — | Defines the profit percentage that activates the rule. |
| `close_percentage` | decimal | no | — | — | no | — | — | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the partial rule is active. |
| `description` | string | yes | — | — | no | — | — | Describes the partial rule. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `partial_group_id` → Partial Group.`id`
- **Uniqueness Constraints:** (`name`); (`partial_group_id`, `profit_percentage`)
- **Indexes:** none

### Action Group

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

Published as `ActionGroup`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `user_id` | integer | no | — | — | no | — | — | Identifies the user who owns the action group. |
| `name` | string | no | — | — | no | — | — | The action group's display name. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the action group is active. |
| `description` | string | yes | — | — | no | — | — | Describes the action group. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Action

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

Published as `Action`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `name` | string | no | — | — | no | — | — | The action's display name. |
| `action_group_id` | integer | no | — | — | no | — | — | Identifies the action group that contains the action. |
| `asset_id` | integer | no | — | — | no | — | — | Identifies the asset traded by the action. |
| `account_id` | integer | no | — | — | no | — | — | Identifies the account used to execute the action. |
| `partial_group_id` | integer | no | — | — | no | — | — | Identifies the Partial Group used by the action. |
| `trailing_group_id` | integer | no | — | — | no | — | — | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | decimal | no | — | — | no | — | — | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | decimal | no | — | — | no | — | — | Defines the Take Profit value used by the action. |
| `stop_loss` | decimal | no | — | — | no | — | — | Defines the Stop Loss value used by the action. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the action is active. |
| `description` | string | yes | — | — | no | — | — | Describes the action. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `action_group_id` → Action Group.`id`; `asset_id` → Asset.`id`; `account_id` → Account.`id`; `partial_group_id` → Partial Group.`id`; `trailing_group_id` → Trailing Group.`id`
- **Uniqueness Constraints:** (`action_group_id`, `name`)
- **Indexes:** none

### Position

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

Published as `Position`.

| Field | Type | Nullable | Default | Sensitivity | Immutable | Generation | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | — | yes | auto_increment | — | — |
| `user_id` | integer | no | — | — | no | — | — | Identifies the user who owns the position. |
| `name` | string | no | — | — | no | — | — | The position's display name. |
| `trading_platform_id` | integer | no | — | — | no | — | — | Identifies the trading platform used to execute the position. |
| `broker_id` | integer | no | — | — | no | — | — | Identifies the broker through which the position is executed. |
| `account_id` | integer | no | — | — | no | — | — | Identifies the trading account used for the position. |
| `trailing_group_id` | integer | no | — | — | no | — | — | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | integer | no | — | — | no | — | — | Identifies the Partial Group applied to the position. |
| `action_group_id` | integer | no | — | — | no | — | — | Identifies the Action Group associated with the position. |
| `action_id` | integer | no | — | — | no | — | — | Identifies the action from which the position is created. |
| `date` | datetime | no | — | — | no | — | — | Stores the position's date and time. |
| `volume` | decimal | no | — | — | no | — | — | Stores the position's trading volume. |
| `profit` | decimal | no | `0` | — | no | — | — | Stores the position's current profit or loss. |
| `is_executed` | boolean | no | `false` | — | no | — | — | Indicates whether the position has been executed. |
| `order_type` | string | no | — | — | no | — | — | Stores the position's order type. |
| `base_tp` | decimal | no | — | — | no | — | — | Stores the position's initial Take Profit value. |
| `base_sl` | decimal | no | — | — | no | — | — | Stores the position's initial Stop Loss value. |
| `real_tp` | decimal | no | — | — | no | — | — | Stores the position's current Take Profit value. |
| `real_sl` | decimal | no | — | — | no | — | — | Stores the position's current Stop Loss value. |
| `is_active` | boolean | no | `true` | — | no | — | — | Indicates whether the position is active. |
| `description` | string | yes | — | — | no | — | — | Describes the position. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`; `trading_platform_id` → Trading Platform.`id`; `broker_id` → Broker.`id`; `account_id` → Account.`id`; `trailing_group_id` → Trailing Group.`id`; `partial_group_id` → Partial Group.`id`; `action_group_id` → Action Group.`id`; `action_id` → Action.`id`
- **Uniqueness Constraints:** (`name`)
- **Indexes:** none

## Declaration

Every Entity publishes its complete logical meaning as `Entity.Declaration`, structured data with no behaviour. An Entity Declaration exposes `name`, `description`, ordered `fields`, `primary_key`, `relations`, `unique_constraints`, and `indexes`. A Field Declaration exposes `name`, `description`, `type`, `nullable`, `has_default` with `default`, `sensitivity`, `immutable`, `constraints`, and `value_generation`. `has_default` distinguishes an absent default from an explicit `null` default.

```python
from model import Account

declaration = Account.Declaration

print(declaration.name)
print([field.name for field in declaration.fields])
print(declaration.primary_key)
for relation in declaration.relations:
    print(relation.local_field, "->", relation.target_entity, relation.target_field)
print(declaration.unique_constraints)
print(declaration.indexes)

password = next(field for field in declaration.fields if field.name == "password")
print(password.type, password.nullable, password.sensitivity, password.immutable)
print(password.has_default, password.default, password.value_generation, dict(password.constraints))
```

Output:

```text
Account
['id', 'name', 'group_id', 'broker_id', 'instance_id', 'base_currency_id', 'username', 'password', 'leverage', 'balance', 'account_type', 'is_active', 'description']
id
group_id -> Account Group id
broker_id -> Broker id
instance_id -> Instance id
base_currency_id -> Currency id
(('name',), ('group_id', 'broker_id', 'instance_id'))
()
string False password False
False None None {}
```

## Foundation

Every Entity exposes the shared conversion capabilities `to_json()` and `from_json()`. A JSON Object is a decoded mapping of Field names to values, not JSON text.

`to_json()` returns a decoded JSON Object: exactly the Field names, in Declaration order. Decimal values travel as text, datetime values as ISO 8601 text, and a pending generated identity as `null`.

```python
from decimal import Decimal

from model import Account

account = Account(
    name="Acc-1",
    group_id=1,
    broker_id=1,
    instance_id=1,
    base_currency_id=1,
    username="example",
    password="placeholder",
    leverage=100,
    account_type="cfd",
    balance=Decimal("10.50"),
)
json_object = account.to_json()
print(json_object)
```

Output:

```text
{'id': None, 'name': 'Acc-1', 'group_id': 1, 'broker_id': 1, 'instance_id': 1, 'base_currency_id': 1, 'username': 'example', 'password': 'placeholder', 'leverage': 100, 'balance': '10.50', 'account_type': 'cfd', 'is_active': True, 'description': None}
```

`Account.from_json(...)` rebuilds an Entity and enforces the same Field contracts as direct construction. Omitted optional Fields take their declared default or `null`.

```python
from model import Account

json_object = {
    "name": "Acc-1", "group_id": 1, "broker_id": 1, "instance_id": 1, "base_currency_id": 1,
    "username": "example", "password": "placeholder", "leverage": 100, "account_type": "cfd",
    "balance": "10.50",
}
account = Account.from_json(json_object)
print(account.balance, account.is_active, account.id)
```

Output:

```text
10.50 True None
```

A complete Entity → JSON Object → Entity round trip. Encoding the Object as JSON text with `json` is the caller's responsibility; Model converts only to and from the decoded Object.

```python
import json
from decimal import Decimal

from model import Account

account = Account(
    name="Acc-1", group_id=1, broker_id=1, instance_id=1, base_currency_id=1,
    username="example", password="placeholder", leverage=100, account_type="cfd",
    balance=Decimal("10.50"),
)
account.id = 42  # assigned once by the owner of the identity

json_object = account.to_json()
text = json.dumps(json_object)  # text encoding is outside Model
restored = Account.from_json(json.loads(text))

print(restored.to_json() == json_object)
print(restored.id, restored.balance, type(restored.balance).__name__)
```

Output:

```text
True
42 10.50 Decimal
```

## Setup

Requirements: Python 3.14 or newer and [uv](https://docs.astral.sh/uv/).

1. From the Component root, create the isolated environment and install the locked dependencies:

   ```text
   uv sync
   ```

2. To use Model from another project, add it as a path dependency:

   ```text
   uv add ../model
   ```

The runtime dependencies are `pydantic` and `sqlmodel`, pinned to exact versions; the quality tools `ruff` and `pyright` are development-only.

## Use

- **Construct** an Entity with keyword arguments. Every Field contract is enforced strictly and without coercion: an integer is not a decimal or a float, a boolean is not an integer, a datetime must carry a time zone, and unknown Fields are rejected.
- **Mutate** a mutable Field by assignment. The new value is validated first; a failed assignment leaves the prior value unchanged. Deleting a declared Field is refused, and `model_copy(update=...)` (and the deprecated `copy(update=...)`) applies each updated value through the same assignment rules; a copy always includes every Field, so `include` and `exclude` are refused.
- **Identity.** `id` is generated by its owner. Omit it when constructing; it reads `None` while pending. It cannot be supplied at construction (`model_validate`, an object carrying an `id` attribute, and JSON validation included). Assign it once, as an integer; afterwards it is immutable.
- **Outside the contract.** Pydantic's deliberately non-validating `model_construct` (and the deprecated `construct`) perform no validation and are not part of Model's contract; do not use them for Entities whose Field contracts matter.
- **Sensitive Fields.** Fields marked `password` or `sensitive` keep their actual value unchanged; the marker is exposed through the Declaration. Model never encrypts, hashes, masks, or redacts a value, and never includes one in an error message.
- **Relations** are metadata only. Model does not resolve, load, or enforce them.
- **Storage and behaviour** belong to other Components; Model publishes only the shared meaning they use.

Realization choices recorded here so later work can rely on them:

- Each Entity is a non-table SQLModel class, so Model assigns no storage or table ownership.
- The `password` Fields carry the `password` marker and the `api_key` Fields carry the `sensitive` marker.
- `Currency.code` declares a Size of 3 and is enforced as exactly three characters.
- Decimal Fields hold `decimal.Decimal` and datetime Fields hold time-zone-aware `datetime` values; both are finite-only and travel through the JSON Object as text. Decimal text must be plain (`"10.50"`, `"-0.5"`, `"1E+2"`): surrounding whitespace, underscores, and non-ASCII digits are rejected.
- Float Fields hold only `float` values and are finite-only. Direct construction and assignment refuse anything that is not already a `float` (an integer, a `Decimal`, a `Fraction`, ...), so no value is silently converted; a JSON Object may carry a whole number for a float Field only when it is exactly representable, and it is restored as a `float`.
- A JSON Object may carry a generated identity: `null` restores a pending identity and an integer restores an assigned one.
- A validation failure raised through an Entity's own methods (construction, assignment, `model_copy`, `model_validate`, `model_validate_json`, `model_validate_strings`, and `from_json`) never carries the caller's input: `str(error)`, `error.errors()`, and `error.json()` hold locations and messages only, including for text that is not valid JSON.
- Pydantic entry points that never reach the Entity — `TypeAdapter`, an Entity's raw `__pydantic_validator__`, and the deprecated `parse_raw` — validate the same Fields but report the raw text when it cannot be parsed as JSON: in `errors()` and `json()` for `TypeAdapter` and the raw validator, and additionally in `str()` and `repr()` for `parse_raw`. Use the Entity's own methods whenever the text may hold a sensitive value.

## Verify

Run the following from the Component root (it changes no Model file):

```text
uv run python - <<'PY'
from decimal import Decimal

from model import User, Account

user = User(name="Ada", username="ada", password="placeholder", api_key="placeholder")
print(user.is_active, user.id)

declaration = User.Declaration
print(declaration.name, declaration.primary_key, [f.name for f in declaration.fields][:3])

account = Account(
    name="Acc-1", group_id=1, broker_id=1, instance_id=1, base_currency_id=1,
    username="example", password="placeholder", leverage=100, account_type="cfd",
    balance=Decimal("1.50"),
)
account.id = 1
assert Account.from_json(account.to_json()).to_json() == account.to_json()
print("round trip ok")
PY
```

Expected output:

```text
True None
User id ['id', 'name', 'username']
round trip ok
```

It checks public import, construction of a representative Entity, access to its Declaration, and a lossless JSON Object round trip.

## Troubleshooting

- **`Field id is generated and cannot be supplied.`** Omit `id` when constructing. It is generated by its owner; assign it afterwards, once.
- **`Field cannot be changed.`** `id` is immutable once assigned.
- **`Input should be a valid ...` or `Input should be an instance of Decimal` on a value that looks right.** Field contracts are strict. Pass a `decimal.Decimal` for decimals, an `int` for integers (not a `bool`), a time-zone-aware `datetime` for datetimes, and text for strings.
- **`Input should be a float.`** A float Field refuses anything that is not already a `float` so that no value is converted silently. Pass `1.0`, not `1` or a `Decimal`.
- **`Extra inputs are not permitted`.** A keyword or JSON Object key is not a declared Field.
- **`from_json` rejects a decimal or datetime.** In a JSON Object, decimals and datetimes are text (`"10.50"`, an ISO 8601 string with a time zone), not numbers.
- **`TypeError: ... differs from its Declaration` at import.** Only when an Entity is edited: its annotated Fields and its Declaration must describe the same Fields, in the same order.
- **Installation fails on an old Python.** Model needs Python 3.14 or newer; `uv` can provide one.

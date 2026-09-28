# Model

Reusable data-model library that defines the Trading Assistant Entities. Each Entity is a flat, technology-independent definition with its Fields, Field Rules, and Entity Metadata, published through one Interface.

```python
from model.interface import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(currency.code)
```

```text
USD
```

## Interface

`model.interface` publishes the actual definition of every Entity, in this order. Loading it creates no Entity and has no external effect.

### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `name` | string | yes | no | none | none | no | none | none | The user's display name. |
| `username` | string | yes | no | none | none | no | none | none | The username used to identify the user. |
| `password` | string | yes | no | none | none | no | none | none | The password credential used by the user. |
| `api_key` | string | yes | no | none | none | no | none | none | The API key assigned to the user. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the user is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the user. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** (`name`); (`username`)
- **Indexes:** none

### Trading Platform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `name` | string | yes | no | none | none | no | none | none | The platform's display name. |
| `code` | string | yes | no | none | none | no | none | none | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the platform is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the platform. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** (`name`)
- **Indexes:** none

### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `user_id` | integer | yes | no | none | none | no | none | none | Identifies the user who owns this instance. |
| `trading_platform_id` | integer | yes | no | none | none | no | none | none | Identifies the trading platform used by this instance. |
| `name` | string | yes | no | none | none | no | none | none | The instance's display name. |
| `ip` | string | no | yes | none | none | no | none | none | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | string | no | yes | none | none | no | none | none | Defines the technical username used to establish the Instance connection when required. |
| `password` | string | no | yes | none | none | no | none | none | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | string | no | yes | none | none | no | none | none | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the instance is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the instance. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`; `trading_platform_id` → Trading Platform.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `user_id` | integer | yes | no | none | none | no | none | none | Identifies the user who owns this currency. |
| `code` | string | yes | no | none | none | no | length ≤ 3 | none | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | string | no | yes | none | none | no | none | none | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | string | no | yes | none | none | no | none | none | Identifies the country or region associated with the currency. |
| `decimal_digits` | integer | no | no | `2` | none | no | none | none | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the currency is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the currency. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `code`)
- **Indexes:** none

### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `name` | string | yes | no | none | none | no | none | none | The broker's display name. |
| `user_id` | integer | yes | no | none | none | no | none | none | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the broker is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the broker. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `broker_id` | integer | yes | no | none | none | no | none | none | Identifies the broker that provides this asset. |
| `symbol` | string | yes | no | none | none | no | none | none | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | string | yes | no | none | none | no | none | none | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | float | no | no | `0.0` | none | no | none | none | Stores the size of one point for the asset. |
| `digits` | integer | no | no | `0` | none | no | none | none | Stores the number of decimal digits used for the asset's price. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the asset is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the asset. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `broker_id` → Broker.`id`
- **Uniqueness Constraints:** (`broker_id`, `symbol`)
- **Indexes:** none

### Account Group

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `user_id` | integer | yes | no | none | none | no | none | none | Identifies the user who owns the account group. |
| `name` | string | yes | no | none | none | no | none | none | The account group's display name. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the account group is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the account group. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `name` | string | yes | no | none | none | no | none | none | The account's display name. |
| `group_id` | integer | yes | no | none | none | no | none | none | Identifies the account group that contains the account. |
| `broker_id` | integer | yes | no | none | none | no | none | none | Identifies the broker that owns the account. |
| `instance_id` | integer | yes | no | none | none | no | none | none | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | yes | no | none | none | no | none | none | Identifies the base currency used by the account. |
| `username` | string | yes | no | none | none | no | none | none | The username identifier used to access the trading account. |
| `password` | string | yes | no | none | none | no | none | none | The credential used to access the trading account. |
| `leverage` | integer | yes | no | none | none | no | none | none | Defines the account's leverage multiplier. |
| `balance` | decimal | no | no | `0` | none | no | none | none | Stores the account's current balance. |
| `account_type` | string | yes | no | none | none | no | none | none | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the account is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the account. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `group_id` → Account Group.`id`; `broker_id` → Broker.`id`; `instance_id` → Instance.`id`; `base_currency_id` → Currency.`id`
- **Uniqueness Constraints:** (`name`); (`group_id`, `broker_id`, `instance_id`)
- **Indexes:** none

### Trailing Group

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `user_id` | integer | yes | no | none | none | no | none | none | Identifies the user who owns the trailing group. |
| `name` | string | yes | no | none | none | no | none | none | The trailing group's display name. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the trailing group is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the trailing group. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Trailing Rule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `name` | string | yes | no | none | none | no | none | none | The trailing rule's display name. |
| `trailing_group_id` | integer | yes | no | none | none | no | none | none | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | decimal | yes | no | none | none | no | none | none | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | decimal | no | yes | none | none | no | none | none | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | decimal | no | yes | none | none | no | none | none | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the trailing rule is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the trailing rule. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `trailing_group_id` → Trailing Group.`id`
- **Uniqueness Constraints:** (`name`); (`trailing_group_id`, `trigger_percentage`)
- **Indexes:** none

### Partial Group

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `user_id` | integer | yes | no | none | none | no | none | none | Identifies the user who owns the partial group. |
| `name` | string | yes | no | none | none | no | none | none | The partial group's display name. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the partial group is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the partial group. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Partial Rule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `name` | string | yes | no | none | none | no | none | none | The partial rule's display name. |
| `partial_group_id` | integer | yes | no | none | none | no | none | none | Identifies the partial group that contains the rule. |
| `profit_percentage` | decimal | yes | no | none | none | no | none | none | Defines the profit percentage that activates the rule. |
| `close_percentage` | decimal | yes | no | none | none | no | none | none | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the partial rule is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the partial rule. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `partial_group_id` → Partial Group.`id`
- **Uniqueness Constraints:** (`name`); (`partial_group_id`, `profit_percentage`)
- **Indexes:** none

### Action Group

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `user_id` | integer | yes | no | none | none | no | none | none | Identifies the user who owns the action group. |
| `name` | string | yes | no | none | none | no | none | none | The action group's display name. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the action group is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the action group. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Action

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `name` | string | yes | no | none | none | no | none | none | The action's display name. |
| `action_group_id` | integer | yes | no | none | none | no | none | none | Identifies the action group that contains the action. |
| `asset_id` | integer | yes | no | none | none | no | none | none | Identifies the asset traded by the action. |
| `account_id` | integer | yes | no | none | none | no | none | none | Identifies the account used to execute the action. |
| `partial_group_id` | integer | yes | no | none | none | no | none | none | Identifies the Partial Group used by the action. |
| `trailing_group_id` | integer | yes | no | none | none | no | none | none | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | decimal | yes | no | none | none | no | none | none | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | decimal | yes | no | none | none | no | none | none | Defines the Take Profit value used by the action. |
| `stop_loss` | decimal | yes | no | none | none | no | none | none | Defines the Stop Loss value used by the action. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the action is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the action. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `action_group_id` → Action Group.`id`; `asset_id` → Asset.`id`; `account_id` → Account.`id`; `partial_group_id` → Partial Group.`id`; `trailing_group_id` → Trailing Group.`id`
- **Uniqueness Constraints:** (`action_group_id`, `name`)
- **Indexes:** none

### Position

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Required | Nullable | Default Value | Sensitivity | Immutable | Constraints | Value Generation | Description |
|---|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | no | none | none | no | none | auto_increment |  |
| `user_id` | integer | yes | no | none | none | no | none | none | Identifies the user who owns the position. |
| `name` | string | yes | no | none | none | no | none | none | The position's display name. |
| `trading_platform_id` | integer | yes | no | none | none | no | none | none | Identifies the trading platform used to execute the position. |
| `broker_id` | integer | yes | no | none | none | no | none | none | Identifies the broker through which the position is executed. |
| `account_id` | integer | yes | no | none | none | no | none | none | Identifies the trading account used for the position. |
| `trailing_group_id` | integer | yes | no | none | none | no | none | none | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | integer | yes | no | none | none | no | none | none | Identifies the Partial Group applied to the position. |
| `action_group_id` | integer | yes | no | none | none | no | none | none | Identifies the Action Group associated with the position. |
| `action_id` | integer | yes | no | none | none | no | none | none | Identifies the action from which the position is created. |
| `date` | datetime | yes | no | none | none | no | none | none | Stores the position's date and time. |
| `volume` | decimal | yes | no | none | none | no | none | none | Stores the position's trading volume. |
| `profit` | decimal | no | no | `0` | none | no | none | none | Stores the position's current profit or loss. |
| `is_executed` | boolean | no | no | `false` | none | no | none | none | Indicates whether the position has been executed. |
| `order_type` | string | yes | no | none | none | no | none | none | Stores the position's order type. |
| `base_tp` | decimal | yes | no | none | none | no | none | none | Stores the position's initial Take Profit value. |
| `base_sl` | decimal | yes | no | none | none | no | none | none | Stores the position's initial Stop Loss value. |
| `real_tp` | decimal | yes | no | none | none | no | none | none | Stores the position's current Take Profit value. |
| `real_sl` | decimal | yes | no | none | none | no | none | none | Stores the position's current Stop Loss value. |
| `is_active` | boolean | no | no | `true` | none | no | none | none | Indicates whether the position is active. |
| `description` | string | no | yes | none | none | no | none | none | Describes the position. |

**Entity Metadata**

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`; `trading_platform_id` → Trading Platform.`id`; `broker_id` → Broker.`id`; `account_id` → Account.`id`; `trailing_group_id` → Trailing Group.`id`; `partial_group_id` → Partial Group.`id`; `action_group_id` → Action Group.`id`; `action_id` → Action.`id`
- **Uniqueness Constraints:** (`name`)
- **Indexes:** none

## Declaration

Every Entity exposes its complete logical meaning as `declaration`, an instance of `Declaration` from `model.core.declaration`. It holds `name`, `description`, `fields`, `primary_key`, `relations`, `unique_constraints`, and `indexes`. Each Field Declaration holds `name`, `description`, `type`, `nullable`, `has_default` and `default`, `sensitivity`, `immutable`, `constraints`, and `value_generation`. Declaration defines no Entity behaviour; creating one only checks that it is well formed and rejects it otherwise.

Reading the metadata of an Entity:

```python
from model.interface import Currency

declaration = Currency.declaration
print(declaration.primary_key)
for relation in declaration.relations:
    print(relation.local_field, "->", relation.target_entity, relation.target_field)
for unique in declaration.unique_constraints:
    print(unique.fields)
print(declaration.indexes)
```

```text
id
user_id -> User id
('user_id', 'code')
()
```

## Foundation

`Foundation` in `model.core.foundation` provides the two conversion capabilities every Entity inherits. JSON objects use the Field names as keys in Declaration order. Decimal values and datetimes are text (`"0.10"`, `"2026-01-02T03:04:05+00:00"`), and a pending Auto Increment value is `null`.

`to_json` converts an Entity to a JSON object:

```python
from model.interface import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(currency.to_json())
```

```text
{'id': None, 'user_id': 1, 'code': 'USD', 'symbol': '$', 'country': 'United States', 'decimal_digits': 2, 'is_active': True, 'description': None}
```

`from_json` constructs an Entity from a JSON object under the same rules as direct construction:

```python
from model.interface import Currency

currency = Currency.from_json({"user_id": 1, "code": "EUR"})
print(currency.code, currency.decimal_digits, currency.is_active)
```

```text
EUR 2 True
```

A complete example using both capabilities with one Entity:

```python
import json

from model.interface import Currency

original = Currency(user_id=1, code="USD", symbol="$", country="United States")
text = json.dumps(original.to_json())
restored = Currency.from_json(json.loads(text))
print(restored.to_json() == original.to_json(), restored.code)
```

```text
True USD
```

## Setup

The Model needs Python 3.14 or newer and [uv](https://docs.astral.sh/uv/).

1. Open a terminal in the Model directory.
2. Run `uv sync` to create the environment and install the locked dependencies.
3. Check the installation with `uv run python -c "from model.interface import User; print(User.declaration.name)"`, which prints `User`.

To use the Model from another project, add it with `uv add <path to the Model directory>`.

## Use

- Import Entities from `model.interface`, and `Declaration` and `Foundation` from `model.core.declaration` and `model.core.foundation`. Do not import from `model.entity` or other modules.
- Construct an Entity with keyword arguments named after its Fields. Omitted Fields resolve as declared: a Default Value applies, a nullable Field becomes `null`, and an Auto Increment `id` stays `None` until storage assigns it.
- Assign to a Field to change it. The new value is validated first, and a rejected assignment leaves the old value in place. `id` cannot change once it has a value.
- Read the meaning of an Entity from `Entity.declaration`, and convert with `to_json` and `from_json`.

```python
from model.interface import Currency

currency = Currency(user_id=1, code="USD")
currency.symbol = "$"
print(currency.symbol, currency.declaration.name)
```

```text
$ Currency
```

## Troubleshooting

Every rejection raises `ValueError` and names the Entity and Field. Messages never contain a Field value.

| Message | Cause | Resolution |
|---|---|---|
| `Currency: unknown Field colour` | A Field that the Entity does not declare was supplied. | Remove it or correct its name. |
| `Currency.user_id: is required` | A Required Field was omitted. | Supply the Field. |
| `Currency.code: must not be null` | `None` was supplied for a non-nullable Field. | Supply a value. |
| `Currency.user_id: must be of type integer` | The value has the wrong type; nothing is converted, and `bool` is not an integer. | Supply a value of the declared Type. |
| `Currency.code: must not exceed 3 characters` | A value breaks a declared constraint. | Supply a value that satisfies the constraint. |
| `Currency.id: is immutable` | A Field that cannot change was assigned a different value. | Do not change the Field. |
| `Currency: JSON must be an object with text keys` | `from_json` received something other than an object with text keys. | Pass the object that `to_json` produced. |
| `Position.date: is not a valid datetime representation` | A JSON datetime is not ISO 8601 text, or a JSON decimal is not text. | Use text such as `"2026-01-02T03:04:05+00:00"`. |
| `Position.date: must be of type datetime` | A datetime has no time zone offset. | Include an offset. |

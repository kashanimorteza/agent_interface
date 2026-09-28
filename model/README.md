# Model

Model is the reusable library of the Trading Assistant's data-model Entities. Each Entity is a flat, independently understandable definition of one domain concept, with its Fields, References, and rules. Model defines Entities only; it does not store, transport, or orchestrate anything.

## Overview

Every Entity is obtained from the Interface layer and behaves as an ordinary object.

```python
from model.interface import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(currency.code, currency.decimal_digits)
```

```text
USD 2
```

Model has four public layers:

| Layer | Purpose |
|---|---|
| `model.interface` | The standard entry point that publishes every Entity. |
| `model.entity` | One unit for each Entity. |
| `model.declaration` | The technology-independent meaning and metadata of every Entity: Types, Field Rules, Primary Key, References, Uniqueness Constraints, Indexes, and Value Generation. |
| `model.foundation` | Shared capabilities of every Entity: conversion to JSON and construction from JSON. |

## Interface

`model.interface` publishes the following Entities. Every Entity has an integer `id` that identifies it, and every Reference holds the `id` of the Entity it names.

### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `name` | string | no |  | unique | The user's display name. |
| `username` | string | no |  | unique | The username used to identify the user. |
| `password` | string | no |  | sensitivity marker `password` | The password credential used by the user. |
| `api_key` | string | no |  | sensitivity marker `sensitive` | The API key assigned to the user. |
| `is_active` | boolean | no | `True` |  | Indicates whether the user is active. |
| `description` | string | yes |  |  | Describes the user. |

### Trading Platform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `name` | string | no |  | unique | The platform's display name. |
| `code` | string | no |  |  | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | boolean | no | `True` |  | Indicates whether the platform is active. |
| `description` | string | yes |  |  | Describes the platform. |

### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `user_id` | integer | no |  | references User `id` | Identifies the user who owns this instance. |
| `trading_platform_id` | integer | no |  | references Trading Platform `id` | Identifies the trading platform used by this instance. |
| `name` | string | no |  |  | The instance's display name. |
| `ip` | string | yes |  |  | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | string | yes |  |  | Defines the technical username used to establish the Instance connection when required. |
| `password` | string | yes |  | sensitivity marker `password` | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | string | yes |  | sensitivity marker `sensitive` | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | no | `True` |  | Indicates whether the instance is active. |
| `description` | string | yes |  |  | Describes the instance. |

Unique combinations: (`user_id`, `name`).

### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `user_id` | integer | no |  | references User `id` | Identifies the user who owns this currency. |
| `code` | string | no |  | length 3 | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | string | yes |  |  | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | string | yes |  |  | Identifies the country or region associated with the currency. |
| `decimal_digits` | integer | no | `2` |  | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | no | `True` |  | Indicates whether the currency is active. |
| `description` | string | yes |  |  | Describes the currency. |

Unique combinations: (`user_id`, `code`).

### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `name` | string | no |  |  | The broker's display name. |
| `user_id` | integer | no |  | references User `id` | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | no | `True` |  | Indicates whether the broker is active. |
| `description` | string | yes |  |  | Describes the broker. |

Unique combinations: (`user_id`, `name`).

### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `broker_id` | integer | no |  | references Broker `id` | Identifies the broker that provides this asset. |
| `symbol` | string | no |  |  | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | string | no |  |  | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | float | no | `0.0` |  | Stores the size of one point for the asset. |
| `digits` | integer | no | `0` |  | Stores the number of decimal digits used for the asset's price. |
| `is_active` | boolean | no | `True` |  | Indicates whether the asset is active. |
| `description` | string | yes |  |  | Describes the asset. |

Unique combinations: (`broker_id`, `symbol`).

### Account Group

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `user_id` | integer | no |  | references User `id` | Identifies the user who owns the account group. |
| `name` | string | no |  |  | The account group's display name. |
| `is_active` | boolean | no | `True` |  | Indicates whether the account group is active. |
| `description` | string | yes |  |  | Describes the account group. |

Unique combinations: (`user_id`, `name`).

### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `name` | string | no |  | unique | The account's display name. |
| `group_id` | integer | no |  | references Account Group `id` | Identifies the account group that contains the account. |
| `broker_id` | integer | no |  | references Broker `id` | Identifies the broker that owns the account. |
| `instance_id` | integer | no |  | references Instance `id` | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | no |  | references Currency `id` | Identifies the base currency used by the account. |
| `username` | string | no |  |  | The username identifier used to access the trading account. |
| `password` | string | no |  | sensitivity marker `password` | The credential used to access the trading account. |
| `leverage` | integer | no |  |  | Defines the account's leverage multiplier. |
| `balance` | decimal | no | `0` |  | Stores the account's current balance. |
| `account_type` | string | no |  |  | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | boolean | no | `True` |  | Indicates whether the account is active. |
| `description` | string | yes |  |  | Describes the account. |

Unique combinations: (`group_id`, `broker_id`, `instance_id`).

### Trailing Group

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `user_id` | integer | no |  | references User `id` | Identifies the user who owns the trailing group. |
| `name` | string | no |  |  | The trailing group's display name. |
| `is_active` | boolean | no | `True` |  | Indicates whether the trailing group is active. |
| `description` | string | yes |  |  | Describes the trailing group. |

Unique combinations: (`user_id`, `name`).

### Trailing Rule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `name` | string | no |  | unique | The trailing rule's display name. |
| `trailing_group_id` | integer | no |  | references Trailing Group `id` | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | decimal | no |  |  | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | decimal | yes |  |  | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | decimal | yes |  |  | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | boolean | no | `True` |  | Indicates whether the trailing rule is active. |
| `description` | string | yes |  |  | Describes the trailing rule. |

Unique combinations: (`trailing_group_id`, `trigger_percentage`).

### Partial Group

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `user_id` | integer | no |  | references User `id` | Identifies the user who owns the partial group. |
| `name` | string | no |  |  | The partial group's display name. |
| `is_active` | boolean | no | `True` |  | Indicates whether the partial group is active. |
| `description` | string | yes |  |  | Describes the partial group. |

Unique combinations: (`user_id`, `name`).

### Partial Rule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `name` | string | no |  | unique | The partial rule's display name. |
| `partial_group_id` | integer | no |  | references Partial Group `id` | Identifies the partial group that contains the rule. |
| `profit_percentage` | decimal | no |  |  | Defines the profit percentage that activates the rule. |
| `close_percentage` | decimal | no |  |  | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | boolean | no | `True` |  | Indicates whether the partial rule is active. |
| `description` | string | yes |  |  | Describes the partial rule. |

Unique combinations: (`partial_group_id`, `profit_percentage`).

### Action Group

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `user_id` | integer | no |  | references User `id` | Identifies the user who owns the action group. |
| `name` | string | no |  |  | The action group's display name. |
| `is_active` | boolean | no | `True` |  | Indicates whether the action group is active. |
| `description` | string | yes |  |  | Describes the action group. |

Unique combinations: (`user_id`, `name`).

### Action

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `name` | string | no |  |  | The action's display name. |
| `action_group_id` | integer | no |  | references Action Group `id` | Identifies the action group that contains the action. |
| `asset_id` | integer | no |  | references Asset `id` | Identifies the asset traded by the action. |
| `account_id` | integer | no |  | references Account `id` | Identifies the account used to execute the action. |
| `partial_group_id` | integer | no |  | references Partial Group `id` | Identifies the Partial Group used by the action. |
| `trailing_group_id` | integer | no |  | references Trailing Group `id` | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | decimal | no |  |  | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | decimal | no |  |  | Defines the Take Profit value used by the action. |
| `stop_loss` | decimal | no |  |  | Defines the Stop Loss value used by the action. |
| `is_active` | boolean | no | `True` |  | Indicates whether the action is active. |
| `description` | string | yes |  |  | Describes the action. |

Unique combinations: (`action_group_id`, `name`).

### Position

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Nullable | Default | Rules | Purpose |
|---|---|---|---|---|---|
| `id` | integer | no |  | primary key; auto increment |  |
| `user_id` | integer | no |  | references User `id` | Identifies the user who owns the position. |
| `name` | string | no |  | unique | The position's display name. |
| `trading_platform_id` | integer | no |  | references Trading Platform `id` | Identifies the trading platform used to execute the position. |
| `broker_id` | integer | no |  | references Broker `id` | Identifies the broker through which the position is executed. |
| `account_id` | integer | no |  | references Account `id` | Identifies the trading account used for the position. |
| `trailing_group_id` | integer | no |  | references Trailing Group `id` | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | integer | no |  | references Partial Group `id` | Identifies the Partial Group applied to the position. |
| `action_group_id` | integer | no |  | references Action Group `id` | Identifies the Action Group associated with the position. |
| `action_id` | integer | no |  | references Action `id` | Identifies the action from which the position is created. |
| `date` | datetime | no |  |  | Stores the position's date and time. |
| `volume` | decimal | no |  |  | Stores the position's trading volume. |
| `profit` | decimal | no | `0` |  | Stores the position's current profit or loss. |
| `is_executed` | boolean | no | `False` |  | Indicates whether the position has been executed. |
| `order_type` | string | no |  |  | Stores the position's order type. |
| `base_tp` | decimal | no |  |  | Stores the position's initial Take Profit value. |
| `base_sl` | decimal | no |  |  | Stores the position's initial Stop Loss value. |
| `real_tp` | decimal | no |  |  | Stores the position's current Take Profit value. |
| `real_sl` | decimal | no |  |  | Stores the position's current Stop Loss value. |
| `is_active` | boolean | no | `True` |  | Indicates whether the position is active. |
| `description` | string | yes |  |  | Describes the position. |

## Foundation

Every Entity converts itself to JSON and is constructed from JSON.

Convert an Entity to JSON:

```python
from model.interface import Currency

currency = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(currency.to_json())
```

Construct an Entity from JSON:

```python
from model.interface import Currency

currency = Currency.from_json('{"user_id": 1, "code": "USD", "decimal_digits": 2}')
print(currency.code, currency.user_id)
```

```text
USD 1
```

Both capabilities together, with one Entity:

```python
from model.interface import Currency

original = Currency(user_id=1, code="EUR", symbol="€", country="Eurozone")
restored = Currency.from_json(original.to_json())
assert restored.code == original.code
assert restored.decimal_digits == original.decimal_digits
print(restored.to_json() == original.to_json())
```

```text
True
```

## Setup

Model needs Python 3.14 or newer and [uv](https://docs.astral.sh/uv/).

```bash
cd model
uv sync
```

Other Components use Model by declaring it as a dependency and importing from `model.interface`.

## Use

Import Entities from `model.interface`, create them with their Fields, and read their declared meaning through `model.declaration`.

```python
from model.declaration import Declaration
from model.interface import Account

declaration = Declaration.of(Account)
print(declaration.primary_key)
print([name for name, reference in declaration.references])
print(declaration.uniques)
```

```text
id
['group_id', 'broker_id', 'instance_id', 'base_currency_id']
(('name',), ('group_id', 'broker_id', 'instance_id'))
```

## Troubleshooting

- `ImportError` for an Entity: import it from `model.interface`, and check that the name is spelled as in the Interface section.
- `ModuleNotFoundError: No module named 'model'`: install the Model package into the environment that runs your code, or run from the Component with `uv run`.
- `from_json` fails or returns unexpected values: pass a JSON object whose keys are Field names; Fields without a Default Value that are neither nullable nor generated must be present.
- A Field with a Reference holds an `id`, not an Entity: create the referenced Entity separately and pass its `id`.

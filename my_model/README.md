# my_model

Reusable data-model library that defines the Trading Assistant's domain Entities. Each Entity is a public table model with a technology-independent `Declaration` of its meaning and the shared JSON conversion supplied by `Foundation`.

## Overview

Import an Entity from the Interface and construct it directly with its Field values:

```python
from my_model.interface import Currency

usd = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(usd.code, usd.decimal_digits)
```

This prints `USD 2`; `decimal_digits` takes its declared default.

## Interface

`my_model.interface` presents every public Entity and the shared capabilities. Every Entity is a table model built on `Foundation`: import it from `my_model.interface`, construct it directly with keyword Fields, and convert it with `to_json()` and `from_json()`. Its meaning is available as `Entity.declaration`.

Table columns: **Nullable** states whether the value may be absent; **Default** is the declared default, `—` when the Field is required.

### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import User`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `name` | string | no | — | unique | The user's display name. |
| `username` | string | no | — | unique | The username used to identify the user. |
| `password` | string | no | — | credential (hash at rest) | The password credential used by the user. |
| `api_key` | string | no | — | credential (hash at rest) | The API key assigned to the user. |
| `is_active` | boolean | no | `True` | — | Indicates whether the user is active. |
| `description` | string | yes | `None` | — | Describes the user. |

### TradingPlatform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import TradingPlatform`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `name` | string | no | — | unique | The platform's display name. |
| `code` | string | no | — | — | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | boolean | no | `True` | — | Indicates whether the platform is active. |
| `description` | string | yes | `None` | — | Describes the platform. |

### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import Instance`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.
- Rule depending on other Entities: The Trading Platform selected through `trading_platform_id` defines which connection fields are required; every field it requires must be present before the Instance can be used.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `user_id` | integer | no | — | references `User.id` | Identifies the user who owns this instance. |
| `trading_platform_id` | integer | no | — | references `TradingPlatform.id` | Identifies the trading platform used by this instance. |
| `name` | string | no | — | — | The instance's display name. |
| `ip` | string | yes | `None` | — | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | string | yes | `None` | — | Defines the technical username used to establish the Instance connection when required. |
| `password` | string | yes | `None` | credential (encrypted at rest) | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | string | yes | `None` | credential (encrypted at rest) | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | no | `True` | — | Indicates whether the instance is active. |
| `description` | string | yes | `None` | — | Describes the instance. |

Combined uniqueness: (`user_id`, `name`).

### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import Currency`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `user_id` | integer | no | — | references `User.id` | Identifies the user who owns this currency. |
| `code` | string | no | — | max length 3 | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | string | yes | `None` | — | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | string | yes | `None` | — | Identifies the country or region associated with the currency. |
| `decimal_digits` | integer | no | `2` | — | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | no | `True` | — | Indicates whether the currency is active. |
| `description` | string | yes | `None` | — | Describes the currency. |

Combined uniqueness: (`user_id`, `code`).

### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import Broker`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `name` | string | no | — | — | The broker's display name. |
| `user_id` | integer | no | — | references `User.id` | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | no | `True` | — | Indicates whether the broker is active. |
| `description` | string | yes | `None` | — | Describes the broker. |

Combined uniqueness: (`user_id`, `name`).

### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import Asset`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `broker_id` | integer | no | — | references `Broker.id` | Identifies the broker that provides this asset. |
| `symbol` | string | no | — | — | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | string | no | — | — | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | float | no | `0.0` | — | Stores the size of one point for the asset. |
| `digits` | integer | no | `0` | — | Stores the number of decimal digits used for the asset's price. |
| `is_active` | boolean | no | `True` | — | Indicates whether the asset is active. |
| `description` | string | yes | `None` | — | Describes the asset. |

Combined uniqueness: (`broker_id`, `symbol`).

### AccountGroup

Defines an independent group for organizing trading accounts owned by one user.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import AccountGroup`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `user_id` | integer | no | — | references `User.id` | Identifies the user who owns the account group. |
| `name` | string | no | — | — | The account group's display name. |
| `is_active` | boolean | no | `True` | — | Indicates whether the account group is active. |
| `description` | string | yes | `None` | — | Describes the account group. |

Combined uniqueness: (`user_id`, `name`).

### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import Account`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.
- Rule depending on other Entities: Instance credentials authenticate the technical Trading Platform connection; Account credentials authenticate this specific trading account. The same credential must not be duplicated across both Models unless the selected Trading Platform explicitly requires it in both roles.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `name` | string | no | — | unique | The account's display name. |
| `group_id` | integer | no | — | references `AccountGroup.id` | Identifies the account group that contains the account. |
| `broker_id` | integer | no | — | references `Broker.id` | Identifies the broker that owns the account. |
| `instance_id` | integer | no | — | references `Instance.id` | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | no | — | references `Currency.id` | Identifies the base currency used by the account. |
| `username` | string | no | — | — | The username identifier used to access the trading account. |
| `password` | string | no | — | credential (encrypted at rest) | The credential used to access the trading account. |
| `leverage` | integer | no | — | — | Defines the account's leverage multiplier. |
| `balance` | decimal | no | `Decimal("0")` | — | Stores the account's current balance. |
| `account_type` | string | no | — | — | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | boolean | no | `True` | — | Indicates whether the account is active. |
| `description` | string | yes | `None` | — | Describes the account. |

Combined uniqueness: (`group_id`, `broker_id`, `instance_id`).

### TrailingGroup

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import TrailingGroup`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `user_id` | integer | no | — | references `User.id` | Identifies the user who owns the trailing group. |
| `name` | string | no | — | — | The trailing group's display name. |
| `is_active` | boolean | no | `True` | — | Indicates whether the trailing group is active. |
| `description` | string | yes | `None` | — | Describes the trailing group. |

Combined uniqueness: (`user_id`, `name`).

### TrailingRule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import TrailingRule`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `name` | string | no | — | unique | The trailing rule's display name. |
| `trailing_group_id` | integer | no | — | references `TrailingGroup.id` | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | decimal | no | — | — | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | decimal | yes | `None` | — | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | decimal | yes | `None` | — | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | boolean | no | `True` | — | Indicates whether the trailing rule is active. |
| `description` | string | yes | `None` | — | Describes the trailing rule. |

Combined uniqueness: (`trailing_group_id`, `trigger_percentage`).

### PartialGroup

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import PartialGroup`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `user_id` | integer | no | — | references `User.id` | Identifies the user who owns the partial group. |
| `name` | string | no | — | — | The partial group's display name. |
| `is_active` | boolean | no | `True` | — | Indicates whether the partial group is active. |
| `description` | string | yes | `None` | — | Describes the partial group. |

Combined uniqueness: (`user_id`, `name`).

### PartialRule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import PartialRule`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `name` | string | no | — | unique | The partial rule's display name. |
| `partial_group_id` | integer | no | — | references `PartialGroup.id` | Identifies the partial group that contains the rule. |
| `profit_percentage` | decimal | no | — | — | Defines the profit percentage that activates the rule. |
| `close_percentage` | decimal | no | — | — | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | boolean | no | `True` | — | Indicates whether the partial rule is active. |
| `description` | string | yes | `None` | — | Describes the partial rule. |

Combined uniqueness: (`partial_group_id`, `profit_percentage`).

### ActionGroup

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import ActionGroup`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `user_id` | integer | no | — | references `User.id` | Identifies the user who owns the action group. |
| `name` | string | no | — | — | The action group's display name. |
| `is_active` | boolean | no | `True` | — | Indicates whether the action group is active. |
| `description` | string | yes | `None` | — | Describes the action group. |

Combined uniqueness: (`user_id`, `name`).

### Action

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import Action`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `name` | string | no | — | — | The action's display name. |
| `action_group_id` | integer | no | — | references `ActionGroup.id` | Identifies the action group that contains the action. |
| `asset_id` | integer | no | — | references `Asset.id` | Identifies the asset traded by the action. |
| `account_id` | integer | no | — | references `Account.id` | Identifies the account used to execute the action. |
| `partial_group_id` | integer | no | — | references `PartialGroup.id` | Identifies the Partial Group used by the action. |
| `trailing_group_id` | integer | no | — | references `TrailingGroup.id` | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | decimal | no | — | — | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | decimal | no | — | — | Defines the Take Profit value used by the action. |
| `stop_loss` | decimal | no | — | — | Defines the Stop Loss value used by the action. |
| `is_active` | boolean | no | `True` | — | Indicates whether the action is active. |
| `description` | string | yes | `None` | — | Describes the action. |

Combined uniqueness: (`action_group_id`, `name`).

### Position

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

- Kind: Domain Entity realized as a table model.
- Import: `from my_model.interface import Position`
- Construction: direct, with keyword Fields.
- JSON conversion: `to_json()` and `from_json()`.

| Field | Type | Nullable | Default | Rules | Purpose |
| --- | --- | --- | --- | --- | --- |
| `id` | integer | no | generated (Auto Increment) | primary key | — |
| `user_id` | integer | no | — | references `User.id` | Identifies the user who owns the position. |
| `name` | string | no | — | unique | The position's display name. |
| `trading_platform_id` | integer | no | — | references `TradingPlatform.id` | Identifies the trading platform used to execute the position. |
| `broker_id` | integer | no | — | references `Broker.id` | Identifies the broker through which the position is executed. |
| `account_id` | integer | no | — | references `Account.id` | Identifies the trading account used for the position. |
| `trailing_group_id` | integer | no | — | references `TrailingGroup.id` | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | integer | no | — | references `PartialGroup.id` | Identifies the Partial Group applied to the position. |
| `action_group_id` | integer | no | — | references `ActionGroup.id` | Identifies the Action Group associated with the position. |
| `action_id` | integer | no | — | references `Action.id` | Identifies the action from which the position is created. |
| `date` | datetime | no | — | — | Stores the position's date and time. |
| `volume` | decimal | no | — | — | Stores the position's trading volume. |
| `profit` | decimal | no | `Decimal("0")` | — | Stores the position's current profit or loss. |
| `is_executed` | boolean | no | `False` | — | Indicates whether the position has been executed. |
| `order_type` | string | no | — | — | Stores the position's order type. |
| `base_tp` | decimal | no | — | — | Stores the position's initial Take Profit value. |
| `base_sl` | decimal | no | — | — | Stores the position's initial Stop Loss value. |
| `real_tp` | decimal | no | — | — | Stores the position's current Take Profit value. |
| `real_sl` | decimal | no | — | — | Stores the position's current Stop Loss value. |
| `is_active` | boolean | no | `True` | — | Indicates whether the position is active. |
| `description` | string | yes | `None` | — | Describes the position. |

## Foundation

`Foundation` is the base of every Entity. It defines no Fields and no domain meaning; it supplies two capabilities that every Entity shares.

### `to_json()`

Convert an instance to JSON text holding every Field value:

```python
from my_model.interface import Currency

usd = Currency(user_id=1, code="USD")
print(usd.to_json())
```

### `from_json()`

Create a validated instance from JSON text (`str` or `bytes`). Omitted Fields take their declared defaults:

```python
from my_model.interface import Currency

usd = Currency.from_json('{"user_id": 1, "code": "USD"}')
print(usd.code, usd.decimal_digits)
```

### Complete example

Both capabilities together with one Entity: convert to JSON and back, and confirm the values are unchanged.

```python
from my_model.interface import Currency

original = Currency(user_id=1, code="EUR", symbol="€", country="Eurozone")
text = original.to_json()
restored = Currency.from_json(text)
print(restored.model_dump() == original.model_dump())
```

## Setup

Requires Python 3.14 or newer and [uv](https://docs.astral.sh/uv/).

Use the library from another project by adding it as a local dependency from that project's directory:

```bash
uv add /path/to/my_model
```

Work on the library itself by installing its locked environment from the library directory:

```bash
uv sync
```

## Run

Model is a library, so there is no process to start. Import it from your own code and run that code through the project's environment (`uv run python your_script.py`). To confirm the library is available, run this from the consumer project:

```bash
uv run python -c "from my_model.interface import User; print(User.declaration.entity)"
```

It prints `User`. To check the library's own source, run these from the library directory:

```bash
uv run ruff format --check src
uv run ruff check src
uv run pyright src
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'my_model'`** — the code ran outside an environment that has the library. Add it with `uv add /path/to/my_model` in the consumer project and start the code with `uv run`.
- **uv reports `No solution found` and names the requested Python version** — the project targets a Python older than 3.14. Use Python 3.14 or newer, for example by creating the consumer project with `uv init --python 3.14`.
- **`NoReferencedTableError` when creating tables** — only some Entity modules were imported before the tables were created, so a referenced Entity is unknown. Import `my_model.interface` first so every Entity is registered.
- **`ValidationError` from `from_json()`** — the JSON omits a required Field or holds a value of the wrong Type. Supply every Field whose Default is `—` in the Interface tables, using values of the declared Type.

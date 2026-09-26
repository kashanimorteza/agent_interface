# my_model

Reusable library of technology-independent Domain Entities for the Trading Assistant.

## Overview

Model defines fifteen flat Domain Entities. Each Entity records its meaning in a `declaration` and converts to and from JSON through Foundation. Every layer is public: the entry point `my_model.model_interface`, each Entity module under `my_model.entity`, `my_model.model_declaration`, and `my_model.model_foundation`.

```python
from my_model.model_interface import Currency

usd = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(usd.code, usd.decimal_digits)
```

Output:

```text
USD 2
```

## Interface

Every public Entity is listed below. Each is a table model imported from `my_model.model_interface`; its Fields follow.

### User

Kind: Entity (table model). Import: `from my_model.model_interface import User`.

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `name` | string | no |  | unique |
| `username` | string | no |  | unique |
| `password` | string | no |  | credential, hash at rest |
| `api_key` | string | no |  | credential, hash at rest |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

### TradingPlatform

Kind: Entity (table model). Import: `from my_model.model_interface import TradingPlatform`.

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `name` | string | no |  | unique |
| `code` | string | no |  |  |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

### Instance

Kind: Entity (table model). Import: `from my_model.model_interface import Instance`.

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `user_id` | integer | no |  | belongs to User.id |
| `trading_platform_id` | integer | no |  | uses TradingPlatform.id |
| `name` | string | no |  |  |
| `ip` | string | yes |  |  |
| `username` | string | yes |  |  |
| `password` | string | yes |  | credential, encrypted at rest |
| `api_key` | string | yes |  | credential, encrypted at rest |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

Unique together: `user_id`, `name`.

### Currency

Kind: Entity (table model). Import: `from my_model.model_interface import Currency`.

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `user_id` | integer | no |  | belongs to User.id |
| `code` | string | no |  | size 3 |
| `symbol` | string | yes |  |  |
| `country` | string | yes |  |  |
| `decimal_digits` | integer | no | 2 |  |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

Unique together: `user_id`, `code`.

### Broker

Kind: Entity (table model). Import: `from my_model.model_interface import Broker`.

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `name` | string | no |  |  |
| `user_id` | integer | no |  | belongs to User.id |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

Unique together: `user_id`, `name`.

### Asset

Kind: Entity (table model). Import: `from my_model.model_interface import Asset`.

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `broker_id` | integer | no |  | belongs to Broker.id |
| `symbol` | string | no |  |  |
| `category` | string | no |  |  |
| `point_size` | float | no | 0.0 |  |
| `digits` | integer | no | 0 |  |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

Unique together: `broker_id`, `symbol`.

### AccountGroup

Kind: Entity (table model). Import: `from my_model.model_interface import AccountGroup`.

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `user_id` | integer | no |  | belongs to User.id |
| `name` | string | no |  |  |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

Unique together: `user_id`, `name`.

### Account

Kind: Entity (table model). Import: `from my_model.model_interface import Account`.

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `name` | string | no |  | unique |
| `group_id` | integer | no |  | belongs to AccountGroup.id |
| `broker_id` | integer | no |  | belongs to Broker.id |
| `instance_id` | integer | no |  | uses Instance.id |
| `base_currency_id` | integer | no |  | uses Currency.id |
| `username` | string | no |  |  |
| `password` | string | no |  | credential, encrypted at rest |
| `leverage` | integer | no |  |  |
| `balance` | decimal | no | 0 |  |
| `account_type` | string | no |  |  |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

Unique together: `group_id`, `broker_id`, `instance_id`.

### TrailingGroup

Kind: Entity (table model). Import: `from my_model.model_interface import TrailingGroup`.

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `user_id` | integer | no |  | belongs to User.id |
| `name` | string | no |  |  |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

Unique together: `user_id`, `name`.

### TrailingRule

Kind: Entity (table model). Import: `from my_model.model_interface import TrailingRule`.

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `name` | string | no |  | unique |
| `trailing_group_id` | integer | no |  | belongs to TrailingGroup.id |
| `trigger_percentage` | decimal | no |  |  |
| `take_profit_adjustment` | decimal | yes |  |  |
| `stop_loss_adjustment` | decimal | yes |  |  |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

Unique together: `trailing_group_id`, `trigger_percentage`.

### PartialGroup

Kind: Entity (table model). Import: `from my_model.model_interface import PartialGroup`.

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `user_id` | integer | no |  | belongs to User.id |
| `name` | string | no |  |  |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

Unique together: `user_id`, `name`.

### PartialRule

Kind: Entity (table model). Import: `from my_model.model_interface import PartialRule`.

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `name` | string | no |  | unique |
| `partial_group_id` | integer | no |  | belongs to PartialGroup.id |
| `profit_percentage` | decimal | no |  |  |
| `close_percentage` | decimal | no |  |  |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

Unique together: `partial_group_id`, `profit_percentage`.

### ActionGroup

Kind: Entity (table model). Import: `from my_model.model_interface import ActionGroup`.

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `user_id` | integer | no |  | belongs to User.id |
| `name` | string | no |  |  |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

Unique together: `user_id`, `name`.

### Action

Kind: Entity (table model). Import: `from my_model.model_interface import Action`.

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `name` | string | no |  |  |
| `action_group_id` | integer | no |  | belongs to ActionGroup.id |
| `asset_id` | integer | no |  | uses Asset.id |
| `account_id` | integer | no |  | uses Account.id |
| `partial_group_id` | integer | no |  | uses PartialGroup.id |
| `trailing_group_id` | integer | no |  | uses TrailingGroup.id |
| `risk_by_reward` | decimal | no |  |  |
| `take_profit` | decimal | no |  |  |
| `stop_loss` | decimal | no |  |  |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

Unique together: `action_group_id`, `name`.

### Position

Kind: Entity (table model). Import: `from my_model.model_interface import Position`.

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

| Field | Type | Nullable | Default | Rules |
| --- | --- | --- | --- | --- |
| `id` | integer | no |  | auto-increment identity |
| `user_id` | integer | no |  | belongs to User.id |
| `name` | string | no |  | unique |
| `trading_platform_id` | integer | no |  | uses TradingPlatform.id |
| `broker_id` | integer | no |  | uses Broker.id |
| `account_id` | integer | no |  | uses Account.id |
| `trailing_group_id` | integer | no |  | uses TrailingGroup.id |
| `partial_group_id` | integer | no |  | uses PartialGroup.id |
| `action_group_id` | integer | no |  | uses ActionGroup.id |
| `action_id` | integer | no |  | belongs to Action.id |
| `date` | date-time | no |  |  |
| `volume` | decimal | no |  |  |
| `profit` | decimal | no | 0 |  |
| `is_executed` | boolean | no | False |  |
| `order_type` | string | no |  |  |
| `base_tp` | decimal | no |  |  |
| `base_sl` | decimal | no |  |  |
| `real_tp` | decimal | no |  |  |
| `real_sl` | decimal | no |  |  |
| `is_active` | boolean | no | True |  |
| `description` | string | yes |  |  |

## Foundation

Foundation gives every Entity two capabilities.

### `to_json`

Converts an instance to JSON text holding every Field value.

```python
from my_model.model_interface import Currency

usd = Currency(user_id=1, code="USD")
print(usd.to_json())
```

Output:

```text
{"user_id":1,"code":"USD","id":null,"symbol":null,"country":null,"decimal_digits":2,"is_active":true,"description":null}
```

### `from_json`

Creates an instance from JSON text. Fields that the JSON omits take their defaults.

```python
from my_model.model_interface import Currency

usd = Currency.from_json('{"user_id": 1, "code": "USD"}')
print(usd.code, usd.decimal_digits)
```

Output:

```text
USD 2
```

### Complete example

Convert an instance to JSON and back.

```python
from my_model.model_interface import Currency

original = Currency(user_id=1, code="EUR", symbol="€", country="Eurozone")
text = original.to_json()
restored = Currency.from_json(text)
print(restored == original)
```

Output:

```text
True
```

## Setup

The library needs Python 3.13 or newer and installs into an isolated environment.

1. Create an isolated environment in the consuming project:

   ```bash
   uv venv --python 3.13
   ```

2. Install the library from its directory (the one that contains `pyproject.toml`):

   ```bash
   uv pip install /path/to/my_model
   ```

3. Confirm the import:

   ```bash
   uv run python -c "import my_model"
   ```

## Run

Model is a library, so nothing runs on its own. After setup, import an Entity from the entry point and construct it directly. Save this as `example.py` in the consuming project:

```python
from my_model.model_interface import Broker

broker = Broker(user_id=1, name="FxPro")
print(broker.name, broker.is_active)
```

Then run it in the isolated environment:

```bash
uv run python example.py
```

Output:

```text
FxPro True
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'my_model'`

The interpreter that ran the code is not the one the library was installed into. Run the code through the
isolated environment with `uv run python ...` from the consuming project, or activate it first with
`source .venv/bin/activate`.

### `No solution found when resolving dependencies` ... `does not satisfy Python>=3.13`

The environment was created with an older Python. Recreate it and install again:

```bash
rm -rf .venv
uv venv --python 3.13
uv pip install /path/to/my_model
```

### `does not appear to be a Python project`

The install path does not contain `pyproject.toml`. Point the install at the `my_model` directory itself, not at a
parent directory:

```bash
uv pip install /path/to/my_model
```

### `ValidationError ... Field required` from `from_json`

The JSON omits a Field that has no default. Include every required Field; the tables in Interface list which Fields
are required (no default and not nullable). For example, a Currency needs `user_id` and `code`:

```python
from my_model.model_interface import Currency

print(Currency.from_json('{"user_id": 1, "code": "USD"}').code)
```

# Model

Model is the shared, technology-independent domain vocabulary of the Trading Assistant. It defines what a
User, Trading Platform, Instance, Currency, Broker, Asset, Account Group, Account, Trailing Group,
Trailing Rule, Partial Group, Partial Rule, Action Group, Action, and Position are: their Fields,
relationships, and constraints.

Model **stores nothing**, performs **no application behaviour**, and offers **no stored-data
operations**. Persistence belongs to the Database Component and application behaviour to the Logic
Component; both read Model only through its Public Interface.

This README documents the implemented Public Interface. It does not replace the Model Definition, the
Target, or the code.

## Interface

Model publishes one Public Interface: the `model` package. Import every Domain Definition from it.

### Operations

Every Domain Definition offers the same Operations.

**Category: Domain Definitions**

| Operation | Accepts | Returns | Outcomes |
|---|---|---|---|
| Construct — `Definition(**fields)` | Every Field by keyword; a Field with a declared default may be omitted, every other Field is required, including a nullable Field (pass `None` explicitly) | A validated instance | Success; `pydantic.ValidationError` when a value, a missing Field, or an unknown Field is not permitted |
| Assign — `instance.field = value` | One Field value | Nothing; the instance is updated | Success; `ValidationError`, with the instance unchanged |
| `instance.serialize()` | Nothing | The Plain Representation: a `dict` of every Field by name. Values are JSON-compatible: a decimal is a string, a date-time is an ISO 8601 string in UTC | Success. It withholds no Field and nests no related definition |
| `Definition.deserialize(data)` | A mapping in Plain Representation | A validated instance | Success; `ValidationError` for a non-mapping, a missing or unknown Field, or a value of a form the definition does not permit |

Validation is strict: nothing is coerced. A string is not accepted for an integer, a float is not
accepted for a decimal, and NaN and infinities are refused. Only `deserialize` accepts the plain string
forms of a decimal and of a date-time. Text Fields have surrounding whitespace removed. A date-time must
carry timezone information and is held in UTC.

**Category: Declaration**

| Operation | Accepts | Returns | Outcomes |
|---|---|---|---|
| `Definition.declaration` | Nothing | A `Declaration`: the definition's Fields, relationships, constraints, and persistence in the Declaration Vocabulary | Success |

A relationship is declared with the referenced definition itself, and in a value it appears only as its
reference (the `*_id` Field). Nullability, whether a Field is required, and its default are exactly those
the Target declares; none is added.

Some Target rules depend on other records and are therefore outside Model, which validates only rules
that need nothing but the definition's own data. Two examples: an Instance's required connection Fields
depend on its Trading Platform, and an Account's credentials must not duplicate its Instance's. The
Component that reads the related records owns them. Model also does not enforce a uniqueness that spans
records; it declares it as a composite constraint or a unique Field.

### Domain Definitions

Every definition below is persistent, is declared in its own module, and is published by name.

### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

Persistence: **persistent**. Import: `from model import User`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the user. |
| `name` | `str` | not null; required; unique | The user's display name. |
| `username` | `str` | not null; required; unique | The username used to identify the user. |
| `password` | `str` | not null; required; credential, hash at rest | The password credential used by the user. |
| `api_key` | `str` | not null; required; credential, hash at rest | The API key assigned to the user. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the user is active. |
| `description` | `str` | nullable; required | Describes the user. |

### TradingPlatform

Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

Persistence: **persistent**. Import: `from model import TradingPlatform`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the trading platform. |
| `name` | `str` | not null; required; unique | The platform's display name. |
| `code` | `str` | not null; required | Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the platform is active. |
| `description` | `str` | nullable; required | Describes the platform. |

### Instance

Defines a user-owned connection instance through which the system accesses a supported Trading Platform.

Persistence: **persistent**. Import: `from model import Instance`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the instance. |
| `user_id` | `int` | not null; required | Identifies the user who owns this instance. |
| `trading_platform_id` | `int` | not null; required | Identifies the trading platform used by this instance. |
| `name` | `str` | not null; required | The instance's display name. |
| `ip` | `str` | nullable; required | Identifies the technical network address used to reach the Trading Platform when required. |
| `username` | `str` | nullable; required | Defines the technical username used to establish the Instance connection when required. |
| `password` | `str` | nullable; required; credential, encrypted at rest | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | `str` | nullable; required; credential, encrypted at rest | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the instance is active. |
| `description` | `str` | nullable; required | Describes the instance. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `user` → `User` (1, required). Belongs to one User through `user_id`.
- `trading_platform` → `TradingPlatform` (1, required). Uses one Trading Platform through `trading_platform_id`.

Composite constraints (declared here, enforced by the Database Component):

- `instance_user_id_name_unique` — The combination of `user_id` and `name` must be unique.

### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

Persistence: **persistent**. Import: `from model import Currency`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the currency. |
| `user_id` | `int` | not null; required | Identifies the user who owns this currency. |
| `code` | `str` | not null; required; length 3 | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | `str` | nullable; required | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | `str` | nullable; required | Identifies the country or region associated with the currency. |
| `decimal_digits` | `int` | not null; default `2` | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the currency is active. |
| `description` | `str` | nullable; required | Describes the currency. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `user` → `User` (1, required). Belongs to one User through `user_id`.

Composite constraints (declared here, enforced by the Database Component):

- `currency_user_id_code_unique` — The combination of `user_id` and `code` must be unique.

### Broker

Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.

Persistence: **persistent**. Import: `from model import Broker`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the broker. |
| `name` | `str` | not null; required | The broker's display name. |
| `user_id` | `int` | not null; required | Identifies the user who owns the broker configuration. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the broker is active. |
| `description` | `str` | nullable; required | Describes the broker. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `user` → `User` (1, required). Belongs to one User through `user_id`.

Composite constraints (declared here, enforced by the Database Component):

- `broker_user_id_name_unique` — The combination of `user_id` and `name` must be unique.

### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

Persistence: **persistent**. Import: `from model import Asset`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the asset. |
| `broker_id` | `int` | not null; required | Identifies the broker that provides this asset. |
| `symbol` | `str` | not null; required | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | `str` | not null; required | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | `float` | not null; default `0.0` | Stores the size of one point for the asset. |
| `digits` | `int` | not null; default `0` | Stores the number of decimal digits used for the asset's price. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the asset is active. |
| `description` | `str` | nullable; required | Describes the asset. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `broker` → `Broker` (1, required). Belongs to one Broker through `broker_id`.

Composite constraints (declared here, enforced by the Database Component):

- `asset_broker_id_symbol_unique` — The combination of `broker_id` and `symbol` must be unique.

### AccountGroup

Defines an independent group for organizing trading accounts owned by one user.

Persistence: **persistent**. Import: `from model import AccountGroup`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the account group. |
| `user_id` | `int` | not null; required | Identifies the user who owns the account group. |
| `name` | `str` | not null; required | The account group's display name. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the account group is active. |
| `description` | `str` | nullable; required | Describes the account group. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `user` → `User` (1, required). Belongs to one User through `user_id`.

Composite constraints (declared here, enforced by the Database Component):

- `account_group_user_id_name_unique` — The combination of `user_id` and `name` must be unique.

### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.

Persistence: **persistent**. Import: `from model import Account`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the account. |
| `name` | `str` | not null; required; unique | The account's display name. |
| `group_id` | `int` | not null; required | Identifies the account group that contains the account. |
| `broker_id` | `int` | not null; required | Identifies the broker that owns the account. |
| `instance_id` | `int` | not null; required | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | `int` | not null; required | Identifies the base currency used by the account. |
| `username` | `str` | not null; required | The username identifier used to access the trading account. |
| `password` | `str` | not null; required; credential, encrypted at rest | The credential used to access the trading account. |
| `leverage` | `int` | not null; required | Defines the account's leverage multiplier. |
| `balance` | `Decimal` | not null; default `Decimal('0')` | Stores the account's current balance. |
| `account_type` | `str` | not null; required | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the account is active. |
| `description` | `str` | nullable; required | Describes the account. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `account_group` → `AccountGroup` (1, required). Belongs to one Account Group through `group_id`.
- `broker` → `Broker` (1, required). Belongs to one Broker through `broker_id`.
- `instance` → `Instance` (1, required). Uses one Instance through `instance_id`.
- `base_currency` → `Currency` (1, required). Uses one Currency as its base currency through `base_currency_id`.

Composite constraints (declared here, enforced by the Database Component):

- `account_group_id_broker_id_instance_id_unique` — The combination of `group_id`, `broker_id`, and `instance_id` must be unique.

### TrailingGroup

Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

Persistence: **persistent**. Import: `from model import TrailingGroup`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the trailing group. |
| `user_id` | `int` | not null; required | Identifies the user who owns the trailing group. |
| `name` | `str` | not null; required | The trailing group's display name. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the trailing group is active. |
| `description` | `str` | nullable; required | Describes the trailing group. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `user` → `User` (1, required). Belongs to one User through `user_id`.

Composite constraints (declared here, enforced by the Database Component):

- `trailing_group_user_id_name_unique` — The combination of `user_id` and `name` must be unique.

### TrailingRule

Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

Persistence: **persistent**. Import: `from model import TrailingRule`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the trailing rule. |
| `name` | `str` | not null; required; unique | The trailing rule's display name. |
| `trailing_group_id` | `int` | not null; required | Identifies the trailing group that contains the rule. |
| `trigger_percentage` | `Decimal` | not null; required | Defines the profit percentage of the take-profit target that activates the rule. |
| `take_profit_adjustment` | `Decimal` | nullable; required | Defines the take-profit adjustment applied when the rule is activated. |
| `stop_loss_adjustment` | `Decimal` | nullable; required | Defines the stop-loss adjustment applied when the rule is activated. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the trailing rule is active. |
| `description` | `str` | nullable; required | Describes the trailing rule. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `trailing_group` → `TrailingGroup` (1, required). Belongs to one Trailing Group through `trailing_group_id`.

Composite constraints (declared here, enforced by the Database Component):

- `trailing_rule_trailing_group_id_trigger_percentage_unique` — The combination of `trailing_group_id` and `trigger_percentage` must be unique.

### PartialGroup

Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

Persistence: **persistent**. Import: `from model import PartialGroup`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the partial group. |
| `user_id` | `int` | not null; required | Identifies the user who owns the partial group. |
| `name` | `str` | not null; required | The partial group's display name. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the partial group is active. |
| `description` | `str` | nullable; required | Describes the partial group. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `user` → `User` (1, required). Belongs to one User through `user_id`.

Composite constraints (declared here, enforced by the Database Component):

- `partial_group_user_id_name_unique` — The combination of `user_id` and `name` must be unique.

### PartialRule

Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

Persistence: **persistent**. Import: `from model import PartialRule`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the partial rule. |
| `name` | `str` | not null; required; unique | The partial rule's display name. |
| `partial_group_id` | `int` | not null; required | Identifies the partial group that contains the rule. |
| `profit_percentage` | `Decimal` | not null; required | Defines the profit percentage that activates the rule. |
| `close_percentage` | `Decimal` | not null; required | Defines the percentage of the position closed when the rule is activated. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the partial rule is active. |
| `description` | `str` | nullable; required | Describes the partial rule. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `partial_group` → `PartialGroup` (1, required). Belongs to one Partial Group through `partial_group_id`.

Composite constraints (declared here, enforced by the Database Component):

- `partial_rule_partial_group_id_profit_percentage_unique` — The combination of `partial_group_id` and `profit_percentage` must be unique.

### ActionGroup

Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

Persistence: **persistent**. Import: `from model import ActionGroup`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the action group. |
| `user_id` | `int` | not null; required | Identifies the user who owns the action group. |
| `name` | `str` | not null; required | The action group's display name. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the action group is active. |
| `description` | `str` | nullable; required | Describes the action group. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `user` → `User` (1, required). Belongs to one User through `user_id`.

Composite constraints (declared here, enforced by the Database Component):

- `action_group_user_id_name_unique` — The combination of `user_id` and `name` must be unique.

### Action

Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

Persistence: **persistent**. Import: `from model import Action`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the action. |
| `name` | `str` | not null; required | The action's display name. |
| `action_group_id` | `int` | not null; required | Identifies the action group that contains the action. |
| `asset_id` | `int` | not null; required | Identifies the asset traded by the action. |
| `account_id` | `int` | not null; required | Identifies the account used to execute the action. |
| `partial_group_id` | `int` | not null; required | Identifies the Partial Group used by the action. |
| `trailing_group_id` | `int` | not null; required | Identifies the Trailing Group used by the action. |
| `risk_by_reward` | `Decimal` | not null; required | Defines the numeric risk-to-reward value used by the action. |
| `take_profit` | `Decimal` | not null; required | Defines the Take Profit value used by the action. |
| `stop_loss` | `Decimal` | not null; required | Defines the Stop Loss value used by the action. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the action is active. |
| `description` | `str` | nullable; required | Describes the action. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `action_group` → `ActionGroup` (1, required). Belongs to one Action Group through `action_group_id`.
- `asset` → `Asset` (1, required). Uses one Asset through `asset_id`.
- `account` → `Account` (1, required). Uses one Account through `account_id`.
- `partial_group` → `PartialGroup` (1, required). Uses one Partial Group through `partial_group_id`.
- `trailing_group` → `TrailingGroup` (1, required). Uses one Trailing Group through `trailing_group_id`.

Composite constraints (declared here, enforced by the Database Component):

- `action_action_group_id_name_unique` — The combination of `action_group_id` and `name` must be unique.

### Position

Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

Persistence: **persistent**. Import: `from model import Position`.

| Field | Type | Properties | Meaning |
|---|---|---|---|
| `id` | `int` | not null; required; identity; generated | The unique identity of the position. |
| `user_id` | `int` | not null; required | Identifies the user who owns the position. |
| `name` | `str` | not null; required; unique | The position's display name. |
| `trading_platform_id` | `int` | not null; required | Identifies the trading platform used to execute the position. |
| `broker_id` | `int` | not null; required | Identifies the broker through which the position is executed. |
| `account_id` | `int` | not null; required | Identifies the trading account used for the position. |
| `trailing_group_id` | `int` | not null; required | Identifies the Trailing Group applied to the position. |
| `partial_group_id` | `int` | not null; required | Identifies the Partial Group applied to the position. |
| `action_group_id` | `int` | not null; required | Identifies the Action Group associated with the position. |
| `action_id` | `int` | not null; required | Identifies the action from which the position is created. |
| `date` | `datetime` (timezone-aware, held in UTC) | not null; required | Stores the position's date and time. |
| `volume` | `Decimal` | not null; required | Stores the position's trading volume. |
| `profit` | `Decimal` | not null; default `Decimal('0')` | Stores the position's current profit or loss. |
| `is_executed` | `bool` | not null; default `False` | Indicates whether the position has been executed. |
| `order_type` | `str` | not null; required | Stores the position's order type. |
| `base_tp` | `Decimal` | not null; required | Stores the position's initial Take Profit value. |
| `base_sl` | `Decimal` | not null; required | Stores the position's initial Stop Loss value. |
| `real_tp` | `Decimal` | not null; required | Stores the position's current Take Profit value. |
| `real_sl` | `Decimal` | not null; required | Stores the position's current Stop Loss value. |
| `is_active` | `bool` | not null; default `True` | Indicates whether the position is active. |
| `description` | `str` | nullable; required | Describes the position. |

Relationships (carried as the referenced definition; a value holds only its reference):

- `user` → `User` (1, required). Belongs to one User through `user_id`.
- `trading_platform` → `TradingPlatform` (1, required). Uses one Trading Platform through `trading_platform_id`.
- `broker` → `Broker` (1, required). Uses one Broker through `broker_id`.
- `account` → `Account` (1, required). Uses one Account through `account_id`.
- `trailing_group` → `TrailingGroup` (1, required). Uses one Trailing Group through `trailing_group_id`.
- `partial_group` → `PartialGroup` (1, required). Uses one Partial Group through `partial_group_id`.
- `action_group` → `ActionGroup` (1, required). Uses one Action Group through `action_group_id`.
- `action` → `Action` (1, required). Belongs to one Action through `action_id`.

### Example: construct and convert

```python
from datetime import datetime, timezone
from decimal import Decimal

from model import Currency, Position

currency = Currency(
    id=1, user_id=1, code="USD", symbol="$", country="United States", decimal_digits=2, description=None
)
plain = currency.serialize()
assert Currency.deserialize(plain) == currency

position = Position(
    id=1, user_id=1, name="Position-1", trading_platform_id=1, broker_id=1, account_id=1,
    trailing_group_id=1, partial_group_id=1, action_group_id=1, action_id=1,
    date=datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc), volume=Decimal("0.10"),
    order_type="buy", base_tp=Decimal("1.2"), base_sl=Decimal("1.1"),
    real_tp=Decimal("1.2"), real_sl=Decimal("1.1"), description=None,
)
print(position.serialize()["date"], position.serialize()["volume"])
```

### Example: credentials

Credentials are held by the caller as already-protected values; Model records only that a Field is a
credential and how it is protected at rest. Use placeholders in documentation and examples, never a
real secret.

```python
from model import User

user = User(
    id=1, name="Admin", username="admin",
    password="<stored-hash-placeholder>", api_key="<stored-hash-placeholder>", description=None,
)
password = next(f for f in User.declaration.fields if f.name == "password")
print(password.sensitivity)  # Sensitivity(classification='credential', at_rest='hash')
```

### Example: read a declaration

```python
from model import Account

declaration = Account.declaration
print(declaration.persistent, [f.name for f in declaration.fields][:3])
for relationship in declaration.relationships:
    print(relationship.name, "->", relationship.definition.__name__)
```

## Setup

Model is a Python library managed with `uv`. From this directory:

```bash
uv sync
```

This creates an isolated environment and installs Pydantic 2.x and the development tools. Configuration:
none; Model reads no environment variables and holds no secret.

## Run

Model is not a process. Consumers import it (`from model import ...`). To try it, run any example above
with `uv run python`.

## Verify

```bash
uv run ruff check
uv run pyright
uv run python -c "import model; print(len([n for n in model.__all__ if hasattr(getattr(model, n), 'declaration')]), 'Domain Definitions')"
```

The last command prints `15 Domain Definitions`.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ValidationError: Field required` | A Field without a declared default was omitted. This includes a nullable Field | Pass every such Field; use `None` for a nullable one |
| `ValidationError: Input should be a valid integer` (or another type) | The value's type is not the Field's type; nothing is coerced | Pass the exact type, for example `Decimal("1.5")` rather than `1.5` |
| `ValidationError: Extra inputs are not permitted` | An unknown Field was given | Remove it, or check the Field name |
| `ValidationError: a date-time must carry timezone information` | A naive `datetime` | Attach a timezone, for example `timezone.utc` |
| `ValidationError: a non-finite decimal is not a valid value` | NaN or an infinity | Pass a finite value |
| `TypeError` when a definition is declared | A Domain Definition lacks a Field's declaration, its persistence, or enforces a different length than it declares | Fix the definition; see `Declare` in the foundation |

# Model

Model is the Trading Assistant's shared domain Model. It is a Python library that other Components import to work with the application's domain data: 15 Domain Definitions (a `User`, a `Position`, and so on), each stating what a domain concept is, which Fields it has, and what properties those Fields carry.

Model stores nothing, performs no application behaviour, and offers no operations on stored data. Saving and finding records belongs to the Database Component, and application behaviour belongs to Logic.

## Package

| | |
|---|---|
| Package name | `model` |
| Public entry point | `import model` |
| Language | Python 3.14 or later |
| Runtime dependency | `pydantic` 2.x |
| Depends on other Components | none |

## Public Interface

Everything a consumer needs is reached from `import model`. Every Domain Definition offers the same four Operations:

| Operation | Accepts | Returns | Outcomes |
|---|---|---|---|
| Construct — `model.User(**fields)` | The Fields of the definition as keyword arguments | A validated instance | An instance, or `model.ValidationError` when a Field is missing, of the wrong type, unknown, or breaks a declared property such as a length |
| Declaration — `model.User.declaration()` | Nothing | A `DefinitionDeclaration` describing the definition | Always succeeds |
| Serialize — `instance.serialize()` | Nothing | A `dict` of simple named values that is JSON-compatible: numbers, strings, booleans, `None`, decimals as strings, datetimes as ISO 8601 strings | Always succeeds for a valid instance |
| Deserialize — `model.User.deserialize(data)` | A `dict` in the shape `serialize` returns: decimals and datetimes as strings | A validated instance | An instance, or `model.ValidationError` when the data breaks any rule construction enforces, including a value of the wrong type or data that is not JSON-compatible |

The package also exports `model.DomainDefinition` (the common base of every definition), `model.DefinitionDeclaration`, `model.FieldDeclaration`, `model.RelationshipDeclaration`, and `model.ValidationError`.

```text
model
├── Domain Definitions (15)
│   ├── construct        model.<Definition>(**fields)
│   ├── declaration      model.<Definition>.declaration()
│   ├── serialize        <instance>.serialize()
│   └── deserialize      model.<Definition>.deserialize(data)
└── Types: DomainDefinition, DefinitionDeclaration, FieldDeclaration, RelationshipDeclaration, ValidationError
```

### Behaviour every Operation shares

- **Generated identity.** Every definition has an `id` that persistence generates. It is `None` on a new instance and is never stored as null; its declaration says `nullable: no`. Pass `id` only for a record that already has one.
- **Omitted nullable Fields** resolve to `None`. That is how Model represents "not provided"; it is not a default the Target declared, so the declaration reports `has_default: False` for them.
- **Credential Fields** keep their value exactly as given — whitespace is never trimmed — and are published like any other Field. Removing a credential from a response is the consuming Component's decision, not Model's. Each credential's at-rest treatment (`hash` or `encrypted`) is in its declaration.
- **Relationships** appear only as the referenced record's identifier (for example `user_id`). A related definition is never nested.
- **Construction and `deserialize` apply the same rules.** Both are strict about types: `Account(leverage="100")` and `Account.deserialize({..., "leverage": "100"})` are both rejected, as are `is_active="no"`, `user_id="7"`, and a number where a decimal is expected. The one difference is representation, not rule: a Plain Representation carries decimals as strings (`"0.10"`) and datetimes as ISO 8601 strings (`"2026-01-02T03:04:05+00:00"`), and `deserialize` requires exactly those forms.
- **Rules that need other records are not Model's.** Uniqueness across stored records (the `unique` marks and the composite sets below) and rules such as "the Trading Platform decides which Instance connection Fields are required" are published or left to the Components that can see the other records; Model checks only what a single instance decides.

### The declaration

`declaration()` returns a `DefinitionDeclaration` with `name`, `persistent`, `unique_sets`, and `fields`. Each entry in `fields` is a `FieldDeclaration`:

| Property | Meaning |
|---|---|
| `logical_type` | `integer`, `float`, `string`, `decimal`, `boolean`, or `datetime` — a technology-independent type |
| `length`, `precision` | Size limits, when the Target declares them |
| `nullable` | Whether persistence may store null |
| `has_default`, `default` | The default the Target declares, as a JSON-compatible value |
| `primary_key`, `generated`, `unique` | Identity, generated identity, and single-Field uniqueness |
| `credential_treatment` | `hash` or `encrypted` for a credential Field, otherwise `None` |
| `relationship` | The referenced definition, its field, `cardinality`, and `optional`, or `None` |

### Domain Definitions

Every definition below is persistent.

#### `User`

An independent user of the system; each user can own a separate set of settings. Persistent: **yes**.

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `name` | string | no | unique |
| `username` | string | no | unique |
| `password` | string | no | credential, at-rest treatment `hash` |
| `api_key` | string | no | credential, at-rest treatment `hash` |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `TradingPlatform`

A supported trading API standard, kept independent of any specific exchange or broker. Persistent: **yes**.

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `name` | string | no | unique |
| `code` | string | no | — |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `Instance`

A user-owned connection through which the system reaches a Trading Platform. Persistent: **yes**.
Composite uniqueness: (user_id, name).

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `user_id` | integer | no | references `User.id` (many-to-one) |
| `trading_platform_id` | integer | no | references `TradingPlatform.id` (many-to-one) |
| `name` | string | no | — |
| `ip` | string | yes | — |
| `username` | string | yes | — |
| `password` | string | yes | credential, at-rest treatment `encrypted` |
| `api_key` | string | yes | credential, at-rest treatment `encrypted` |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `Currency`

A currency the trading system can use, with its code, symbol, region, and decimal precision. Persistent: **yes**.
Composite uniqueness: (user_id, code).

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `user_id` | integer | no | references `User.id` (many-to-one) |
| `code` | string | no | length 3 |
| `symbol` | string | yes | — |
| `country` | string | yes | — |
| `decimal_digits` | integer | no | default `2` |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `Broker`

A broker the system supports, owned by one user. Persistent: **yes**.
Composite uniqueness: (user_id, name).

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `name` | string | no | — |
| `user_id` | integer | no | references `User.id` (many-to-one) |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `Asset`

A tradable asset provided by a broker, with its category and price precision. Persistent: **yes**.
Composite uniqueness: (broker_id, symbol).

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `broker_id` | integer | no | references `Broker.id` (many-to-one) |
| `symbol` | string | no | — |
| `category` | string | no | — |
| `point_size` | float | no | default `0.0` |
| `digits` | integer | no | default `0` |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `AccountGroup`

A group that organizes one user's trading accounts. Persistent: **yes**.
Composite uniqueness: (user_id, name).

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `user_id` | integer | no | references `User.id` (many-to-one) |
| `name` | string | no | — |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `Account`

A funded trading account through which trades are executed; it uses an Instance for the technical connection. Persistent: **yes**.
Composite uniqueness: (group_id, broker_id, instance_id).

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `name` | string | no | unique |
| `group_id` | integer | no | references `AccountGroup.id` (many-to-one) |
| `broker_id` | integer | no | references `Broker.id` (many-to-one) |
| `instance_id` | integer | no | references `Instance.id` (many-to-one) |
| `base_currency_id` | integer | no | references `Currency.id` (many-to-one) |
| `username` | string | no | — |
| `password` | string | no | credential, at-rest treatment `encrypted` |
| `leverage` | integer | no | — |
| `balance` | decimal | no | default `0` |
| `account_type` | string | no | — |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `TrailingGroup`

A group of trailing rules that manage Stop Loss and Take Profit during a trade. Persistent: **yes**.
Composite uniqueness: (user_id, name).

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `user_id` | integer | no | references `User.id` (many-to-one) |
| `name` | string | no | — |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `TrailingRule`

One rule that says when and how to adjust Take Profit and Stop Loss. Persistent: **yes**.
Composite uniqueness: (trailing_group_id, trigger_percentage).

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `name` | string | no | unique |
| `trailing_group_id` | integer | no | references `TrailingGroup.id` (many-to-one) |
| `trigger_percentage` | decimal | no | — |
| `take_profit_adjustment` | decimal | yes | — |
| `stop_loss_adjustment` | decimal | yes | — |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `PartialGroup`

A group of rules for closing portions of an open trade. Persistent: **yes**.
Composite uniqueness: (user_id, name).

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `user_id` | integer | no | references `User.id` (many-to-one) |
| `name` | string | no | — |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `PartialRule`

One rule that says at which profit part of a position is closed and how much. Persistent: **yes**.
Composite uniqueness: (partial_group_id, profit_percentage).

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `name` | string | no | unique |
| `partial_group_id` | integer | no | references `PartialGroup.id` (many-to-one) |
| `profit_percentage` | decimal | no | — |
| `close_percentage` | decimal | no | — |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `ActionGroup`

A group of actions organized by risk profile. Persistent: **yes**.
Composite uniqueness: (user_id, name).

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `user_id` | integer | no | references `User.id` (many-to-one) |
| `name` | string | no | — |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `Action`

How a position must be opened: asset, account, risk, Take Profit, Stop Loss, Partial Group, and Trailing Group. Persistent: **yes**.
Composite uniqueness: (action_group_id, name).

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `name` | string | no | — |
| `action_group_id` | integer | no | references `ActionGroup.id` (many-to-one) |
| `asset_id` | integer | no | references `Asset.id` (many-to-one) |
| `account_id` | integer | no | references `Account.id` (many-to-one) |
| `partial_group_id` | integer | no | references `PartialGroup.id` (many-to-one) |
| `trailing_group_id` | integer | no | references `TrailingGroup.id` (many-to-one) |
| `risk_by_reward` | decimal | no | — |
| `take_profit` | decimal | no | — |
| `stop_loss` | decimal | no | — |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |

#### `Position`

A position the system created, opened or still pending. Persistent: **yes**.

| Field | Type | Nullable | Properties |
|---|---|---|---|
| `id` | integer | no | primary key, generated (absent until generated) |
| `user_id` | integer | no | references `User.id` (many-to-one) |
| `name` | string | no | unique |
| `trading_platform_id` | integer | no | references `TradingPlatform.id` (many-to-one) |
| `broker_id` | integer | no | references `Broker.id` (many-to-one) |
| `account_id` | integer | no | references `Account.id` (many-to-one) |
| `trailing_group_id` | integer | no | references `TrailingGroup.id` (many-to-one) |
| `partial_group_id` | integer | no | references `PartialGroup.id` (many-to-one) |
| `action_group_id` | integer | no | references `ActionGroup.id` (many-to-one) |
| `action_id` | integer | no | references `Action.id` (many-to-one) |
| `date` | datetime | no | — |
| `volume` | decimal | no | — |
| `profit` | decimal | no | default `0` |
| `is_executed` | boolean | no | default `False` |
| `order_type` | string | no | — |
| `base_tp` | decimal | no | — |
| `base_sl` | decimal | no | — |
| `real_tp` | decimal | no | — |
| `real_sl` | decimal | no | — |
| `is_active` | boolean | no | default `True` |
| `description` | string | yes | — |


## Setup

Model is installed as a library into the consumer's isolated environment. From the consumer's project:

```bash
uv add ./model
```

To work on Model itself, from the Model directory:

```bash
uv sync
```

Model needs no configuration, no environment variables, and no secrets.

## Use

```python
from datetime import datetime, timezone
from decimal import Decimal

import model

# Construct an instance. `id` is absent until it is generated.
user = model.User(
    name="Admin", username="admin", password="<password>", api_key="<api-key>"
)
assert user.id is None and user.is_active is True

# Read what the definition declares.
declaration = model.User.declaration()
assert declaration.persistent is True
assert declaration.fields["password"].credential_treatment == "hash"
assert declaration.fields["id"].generated is True

# Turn an instance into its Plain Representation.
data = user.serialize()
assert data["username"] == "admin"

# Build an instance back from a Plain Representation.
assert model.User.deserialize(data) == user

# Decimals and datetimes survive the round trip through JSON-compatible values.
position = model.Position(
    user_id=1,
    name="EURUSD-1",
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
    base_tp=Decimal("1.2345"),
    base_sl=Decimal("1.1"),
    real_tp=Decimal("1.2345"),
    real_sl=Decimal("1.1"),
)
assert model.Position.deserialize(position.serialize()) == position

# Invalid data is rejected.
try:
    model.Currency(user_id=1, code="USDD")
except model.ValidationError:
    print("rejected: currency code longer than 3 characters")
```

Encoding the Plain Representation as JSON text is the consumer's step:

```python
import json

text = json.dumps(
    model.User(
        name="Admin", username="admin", password="<password>", api_key="<api-key>"
    ).serialize()
)
```

## Verify

Run the example above; every `assert` passes and the last line prints `rejected: currency code longer than 3 characters`. Model's own quality tools run from its directory:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pyright
```

Model carries no test suite: its verification is these checks and the example.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ValidationError: Extra inputs are not permitted` | A key that is not a Field of the definition was passed | Remove it; check the Field names in the tables above |
| `ValidationError: Input should be a valid integer` when constructing | Construction is strict and a string was given | Pass the exact type (`int`, `Decimal`, `datetime`); `deserialize` is just as strict, and expects decimals and datetimes as strings |
| `ValidationError` on a datetime | The datetime has no timezone | Give it a timezone, for example `tzinfo=timezone.utc` |
| `ValidationError: Field required` | A required Field was left out | Supply it; nullable and defaulted Fields may be omitted |
| `ModuleNotFoundError: No module named 'model'` | Model is not installed in the active environment | Follow Setup, then run with `uv run` |

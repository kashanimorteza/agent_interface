# my_model

The independent, platform-independent domain Model package for the Trading Assistant. It defines the project's domain entities, their fields, relationships, rules, and required initial data, and gives every other technical component (Database, Backend, Frontend) one shared logical understanding of that data.

## Purpose and boundaries

`my_model` owns domain representations, field semantics, conceptual relationships, domain rules that are determinable from a single instance's own data, initial-data declarations, and one stable public package interface.

It does **not** own persistence (tables, columns, foreign keys, migrations), API transport (HTTP routes, request/response contracts), business workflows, or presentation. Those belong to the Database, Backend, and Frontend components, which derive their own representations from this package.

A few rules stated by the project definition require information this package does not have on its own (for example, uniqueness across stored records, or a rule that depends on which trading platform an Instance uses) — these are enforced by the Database and Backend components that hold that information, not by `my_model`.

## Installation

This package uses [uv](https://docs.astral.sh/uv/) for environment and dependency management.

```bash
cd my_model
uv sync
```

This creates an isolated `.venv` and installs `my_model` together with its one runtime dependency, Pydantic 2.

## Public interface

Every domain Model is an Entity Model (there is no Value Object, Enum, Root Model, or Generic Model in this phase) and is exposed exactly once, both as a public submodule and as a re-exported class at the package root:

```text
my_model
├── User
├── TradingPlatform
├── Currency
├── Broker
├── Asset
├── Instance
├── AccountGroup
├── Account
├── TrailingGroup
├── TrailingRule
├── PartialGroup
├── PartialRule
├── ActionGroup
├── Action
└── Position
```

Two supported, equivalent import styles:

```python
# Canonical: module-qualified
import my_model
my_model.user.User(...)

# Alternate: explicit module import
from my_model import user
user.User(...)
```

A Model is always identified by an imported module, Model type, or Model instance — never by a string name or a registry lookup.

## Dependencies

- Python 3.13+
- Pydantic 2.x (the only runtime dependency)

## Configuration

`my_model` has no runtime configuration and no secrets. Every domain Model is a plain, side-effect-free Pydantic model.

## Usage examples

The examples below use `TradingPlatform`, one of the package's Entity Models, to demonstrate the patterns every Model in the package follows.

**Construct a valid instance:**

```python
import my_model

platform = my_model.TradingPlatform(name="Example Platform", code="example")
```

**Validation failure for invalid data:**

```python
from pydantic import ValidationError

try:
    my_model.TradingPlatform(name="Example Platform")  # code is required
except ValidationError as exc:
    print(exc)
```

**Serialization:**

```python
platform.model_dump()
platform.model_dump_json()
```

**Schema generation:**

```python
my_model.TradingPlatform.model_json_schema()
```

**Omitted, explicit `None`, supplied, and default values** (shown with `Currency.symbol`, which is optional, and `Currency.decimal_digits`, which has a declared default):

```python
c1 = my_model.Currency(user_id=1, code="XTS")               # symbol omitted -> None; decimal_digits -> default 2
c2 = my_model.Currency(user_id=1, code="XTS", symbol=None)   # symbol explicitly null
c3 = my_model.Currency(user_id=1, code="XTS", symbol="X")    # symbol supplied
```

A field that is not yet generated (such as every Model's `id`, which is assigned once persisted) is represented as `None` until a value is assigned — this is a distinct state from a field that is genuinely optional in the domain.

**Partial update**, preserving the distinction between "leave unchanged" and "set to null":

```python
updated = platform.model_copy(update={"description": "An updated description."})
```

Only the fields passed to `update` change; every other field, including ones a caller does not mention, keeps its current value.

**Relationships**, using `Account`, which relates to four other Models by identifier:

```python
account = my_model.Account(
    name="Sample Account",
    group_id=1,
    broker_id=1,
    instance_id=1,
    base_currency_id=1,
    username="sample",
    password="sample-secret",
    leverage=100,
    account_type="cfd",
)
```

**Sensitive and credential fields**, using `User.password` and `User.api_key`:

```python
user = my_model.User(name="Example User", username="example", password="hunter2", api_key="abc123")
```

`password` and `api_key` are declared as credential fields. `my_model` never hashes, encrypts, or displays them specially; it only preserves the fact that they are sensitive so that a consumer (such as Database, when storing them, or an API, when serializing a response) knows to handle them accordingly. `model_dump()` includes their plain declared value — masking or protected storage is the responsibility of the component that persists or transmits it, not of this package.

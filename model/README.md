# my_model

The shared logical Model package of Trading Assistant. It defines every domain
Model once and publishes each as one validated class, so the Database, Backend,
and Frontend layers share a single meaning for the project's data.

## Purpose and boundaries

`my_model` owns the fourteen domain Models — their fields, defaults, and the
validation of instances. Other layers import this package; their persistence
mappings and transport schemas are derived from the same project definition and
never restate a Model.

The package does **not** own persistence (tables, foreign keys, migrations,
credential storage, seeding — Database), application behaviour or the API
(Backend), presentation (Frontend), or runtime configuration and deployment
(Platform).

## Public interface

Import only from `my_model`. Each Model is exposed exactly once under its public
symbol:

| Model | Symbol |
| --- | --- |
| User | `User` |
| Currency | `Currency` |
| Trading Platform | `TradingPlatform` |
| Broker | `Broker` |
| Account Group | `AccountGroup` |
| Account | `Account` |
| Asset | `Asset` |
| Trailing Group | `TrailingGroup` |
| Trailing Rule | `TrailingRule` |
| Partial Group | `PartialGroup` |
| Partial Rule | `PartialRule` |
| Action Group | `ActionGroup` |
| Action | `Action` |
| Position | `Position` |

Constructing a Model validates field types, nullability, and defaults; an invalid
value, a missing required field, a null in a non-nullable field, or an unknown
field raises `pydantic.ValidationError`. Two conventions hold for every Model:

- **The primary key is absent until persistence assigns it.** `id` is `None` on a
  Model you construct.
- **Credential values are never carried back.** A credential field (`User.password`,
  `User.api_key`, `Account.password`) is accepted when you construct a Model but is
  `None` on every instance returned from storage; it is required in the domain, so
  supply it on create.

## Dependencies

- Python 3.14.7 (`requires-python >=3.14,<3.15`)
- [pydantic](https://docs.pydantic.dev/) 2.13.5 — the only run-time dependency
- [uv](https://docs.astral.sh/uv/) 0.12.10 — environment and build tool

## Configuration

None. The package reads no configuration and no environment variable.

## Installation and startup

The package is a library; there is nothing to start. From this directory:

```
uv sync
```

A consumer installs it as an editable local path dependency in its `pyproject.toml`:

```toml
[project]
dependencies = ["my-model"]

[tool.uv.sources]
my-model = { path = "../model", editable = true }
```

The distribution is named `my-model` and the import package `my_model`; it is
internal and never published.

## Usage examples

Construct a Model and let it validate itself:

```python
from decimal import Decimal

from my_model import Account

account = Account(
    name="Acc-1",
    group_id=1,
    broker_id=1,
    base_currency_id=1,
    username="test",
    password="secret",   # accepted on create; never returned from storage
    leverage=100,
    account_type="CFD",
)

assert account.id is None                # assigned by persistence on create
assert account.balance == Decimal("0")   # declared default
assert account.status is True            # declared default
```

Invalid values are rejected with the modeling library's own error:

```python
import pydantic

from my_model import Currency

try:
    Currency(name="Yen", code="JPYX")    # code is at most 3 characters
except pydantic.ValidationError as error:
    print("rejected:", error.error_count(), "error(s)")

try:
    Currency(name="Euro")                 # code is required
except pydantic.ValidationError:
    print("rejected: missing code")
```

Every Model is available from the root under its symbol:

```python
import my_model

symbols = ["User", "Currency", "TradingPlatform", "Broker", "AccountGroup", "Account", "Asset",
           "TrailingGroup", "TrailingRule", "PartialGroup", "PartialRule", "ActionGroup", "Action", "Position"]
assert all(hasattr(my_model, s) for s in symbols)
print(len(symbols), "Models")
```

# my_model

The shared Model package of the Trading Assistant. It is the single logical source for the project's domain data: every domain Model, with its fields, relationships, domain rules, and initial data, is declared here once and consumed by every other application layer.

## Purpose and boundaries

`my_model` describes **what the project's data is**. It owns:

- the fourteen domain Models the project defines;
- each Model's fields with their logical properties: type, optionality, uniqueness, default, credential nature, size, and meaning;
- each Model's relationships to other Models;
- each Model's domain rules, such as composite uniqueness and the storage mode a credential must use at rest;
- each Model's initial data, the records that must exist when the project begins;
- validation of a Model value against its declared field properties.

It does **not** own persistence mappings, business behaviour, API transport, user-interface presentation, or deployment. Relationships, rules, and initial data are logical declarations; the layer that stores or exposes a Model resolves and enforces them.

An initial-data value the project marks as generated securely is declared with the `Generate` marker, never as a stored value. The package holds no generated secret; the layer that inserts the initial data generates the value.

## Public interface

Import everything from `my_model`. The package's internal modules are not part of the interface.

Domain Models, in project order:

| Symbol | Logical name |
|---|---|
| `User` | User |
| `Currency` | Currency |
| `TradingPlatform` | Trading Platform |
| `Broker` | Broker |
| `AccountGroup` | Account Group |
| `Account` | Account |
| `Asset` | Asset |
| `TrailingGroup` | Trailing Group |
| `TrailingRule` | Trailing Rule |
| `PartialGroup` | Partial Group |
| `PartialRule` | Partial Rule |
| `ActionGroup` | Action Group |
| `Action` | Action |
| `Position` | Position |

`MODELS` is the tuple of these fourteen classes in the same order.

Modeling support:

| Symbol | Purpose |
|---|---|
| `Model` | Base class of every domain Model. Validation is strict: a value is accepted only when every field holds a value of its declared logical type, every required field is present, and no undeclared field is given. |
| `FieldSpec` | The logical properties of one field, returned by `Model.field_specs()` and `Model.field_spec(name)`. |
| `Relationship` | A connection to another Model carried by one field, with `kind` `belongs_to` or `uses` and an optional `role`. Read from `Model.relationships`. |
| `UniqueTogether` | A rule that the combination of the named fields must be unique. Read from `Model.rules`. |
| `CredentialStorage` | A rule that a credential field must use the named storage mode (`hash` or `encrypted`) at rest. Read from `Model.rules`. |
| `Rule` | The union of the rule types. |
| `Generate` | The marker for an initial-data value that must be generated securely. Appears in `Model.initial_data`. |

Every Model class exposes these class-level declarations:

| Attribute | Meaning |
|---|---|
| `logical_name` | The Model's name as the project states it, for example `Trading Platform`. |
| `field_specs()` | Mapping of field name to `FieldSpec`, in declaration order. |
| `relationships` | Tuple of `Relationship`. |
| `rules` | Tuple of rules. |
| `initial_data` | Tuple of records, each a mapping of field name to value or `Generate`. |

Logical types are `integer`, `string`, `boolean`, `decimal`, `float`, and `datetime`, carried at runtime as `int`, `str`, `bool`, `decimal.Decimal`, `float`, and `datetime.datetime`.

An auto-increment field (`id`) is assigned by the storing layer, so it may be omitted when a value is constructed even though it is logically not nullable.

## Dependencies

- Python 3.14 or later.
- `pydantic` for runtime validation.

The package depends on no other application layer. Its consumers are the Database, Backend, and Frontend layers, which import it through this interface.

## Configuration

The package has no runtime configuration. Its section of the centralized runtime configuration (`model` in the project's `application.yaml`) carries no settings and no bindings, because nothing in the Model layer is changeable by a user or environment. No secret value is read or stored by this package.

## Installation

The package is internal and is not published. Install it from its directory into the consuming environment:

```bash
uv pip install path/to/model
```

Inside the package directory, `uv sync` creates the package's own isolated environment with its dependencies resolved.

There is nothing to start: `my_model` is an importable library.

## Usage

Construct and validate a Model value:

```python
from decimal import Decimal
from my_model import Account, Currency

usd = Currency(name="US Dollar", code="USD", symbol="$", country="United States")
assert usd.decimal_digits == 2  # default applied

account = Account(
    name="Main",
    group_id=1,
    broker_id=1,
    base_currency_id=1,
    username="trader",
    password="<provided at runtime>",
    leverage=100,
    account_type="cfd",
)
assert account.balance == Decimal("0")
```

Read a Model's logical declarations:

```python
from my_model import Broker, User, TradingPlatform, MODELS, Generate

spec = Broker.field_spec("user_id")
assert spec.type == "integer" and not spec.nullable

targets = {r.field: r.target for r in Broker.relationships}
assert targets == {"user_id": User, "trading_platform_id": TradingPlatform}

assert any(rule.fields == ("user_id", "name") for rule in Broker.rules if hasattr(rule, "fields"))

admin = User.initial_data[0]
assert admin["password"] is Generate  # generated by the inserting layer

assert len(MODELS) == 14
```

A value that violates a declared field property is refused with a validation error:

```python
from pydantic import ValidationError
from my_model import Currency, AccountGroup, Asset, Action, ActionGroup, PartialGroup, PartialRule, Position, TrailingGroup, TrailingRule

try:
    Currency(name="Bad", code="ABCD")  # code is limited to three characters
except ValidationError:
    pass
else:
    raise AssertionError("expected refusal")
```

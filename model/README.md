# my_model

The shared Model package of the Trading Assistant. It is the single logical source for the project's domain data: every domain Model, with its fields, relationships, domain rules, and initial data, is declared here once, and the validation every layer applies to that data lives here too.

## Purpose and boundaries

`my_model` describes **what the project's data is**. It owns:

- the fourteen domain Models the project defines;
- each Model's fields with their logical properties: type, identity, uniqueness, optionality, default behaviour, credential nature, permitted generation, size, and meaning;
- each Model's relationships to other Models;
- each Model's domain rules, such as composite uniqueness and the storage mode a credential must use at rest;
- each Model's initial data, the records that must exist when the project begins;
- the validation of a complete domain state and of a partial change, from what a Model's own data determines.

It does **not** own persistence mappings, business behaviour, API transport, user-interface presentation, or deployment. Validation here never queries storage, calls a service, or performs an operation. Rules that need application context are enforced by the layer running the operation, and rules that need stored state — uniqueness across records, the existence of a referenced record — are guaranteed by the layer that stores the Model. Every such rule is still declared here, so it stays traceable to the Model wherever it is enforced.

Initial data is a logical declaration. A value the project says to generate is marked `Pending`; this package never invents one, and the storing layer supplies it.

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

Declaration support:

| Symbol | Purpose |
|---|---|
| `Model` | Base class of every domain Model. Constructing one validates a complete state strictly. |
| `FieldSpec` | The logical properties of one field, from `Model.field_specs()` or `Model.field_spec(name)`. |
| `Relationship` | A connection to another Model carried by one field, with `kind` `belongs_to` or `uses` and an optional `role`. From `Model.relationships`. |
| `UniqueTogether` | A rule that the combination of the named fields is unique across records. Declared here, guaranteed by the storing layer. From `Model.rules`. |
| `CredentialStorage` | A rule that a credential field uses the named storage mode (`hash` or `encrypted`) at rest. From `Model.rules`. |
| `Rule` | The union of the rule types. |
| `Pending` | The marker for a value awaiting declared generation. Appears in `Model.initial_data`. |

Validation:

| Symbol | Purpose |
|---|---|
| `validate_state(Model, data)` | Validates a complete domain state; returns a `State`. |
| `validate_change(Model, data)` | Validates a partial change; returns a `Change`. |
| `State` | `values` (known values with defaults applied), `pending` (fields awaiting generation), `is_complete`, and `resolved(**generated)` which returns the Model instance. |
| `Change` | `changes` (only the fields actually changing), `pending`, and `is_empty`. |
| `InvalidValue` | Raised when the data does not satisfy the Model's own declarations. Carries `errors` and `fields`. |
| `FieldError` | One reason a value was refused: `field`, `code`, `message`. |

Every Model class exposes these class-level declarations:

| Attribute | Meaning |
|---|---|
| `logical_name` | The Model's name as the project states it, for example `Trading Platform`. |
| `field_specs()` | Mapping of field name to `FieldSpec`, in declaration order. |
| `relationships` | Tuple of `Relationship`. |
| `rules` | Tuple of rules. |
| `initial_data` | Tuple of records, each a mapping of field name to a value or `Pending`. |

Logical types are `integer`, `string`, `boolean`, `decimal`, `float`, and `datetime`, carried at runtime as `int`, `str`, `bool`, `decimal.Decimal`, `float`, and `datetime.datetime`.

### Absent, null, and pending are three different things

Reuse `validate_state` and `validate_change` rather than writing your own checks, so that every layer treats these the same way:

| Situation | In a complete state | In a partial change |
|---|---|---|
| The field is **absent** | Its declared default applies; otherwise its declared generation makes it pending; otherwise it is refused as missing | It is left unchanged |
| The field is **explicitly null** | Accepted only where the field permits null, otherwise refused | The same |
| The field is **`Pending`** | Recorded in `pending`, never given an invented value. Accepted only where the field permits generation | The same |

An auto-increment identifier is assigned by the storing layer, so a caller may omit it from a complete state and may never change it.

## Dependencies

- Python 3.14 or later.
- `pydantic` for runtime validation.

The package depends on no other application layer. Its consumers are the Database, Backend, and Frontend layers, which import it through this interface.

## Configuration

The Model layer owns no runtime setting and consumes no other layer, so both of its configuration files are empty of content:

| File | Holds |
|---|---|
| `model.yaml`, in this package's own directory | The settings the Model layer owns. It has none, so `settings` is empty. |
| `application.yaml`, at the project root, section `model` | The bindings the Model layer consumes. It consumes none, so `bindings` is empty. |

Neither file carries a secret value, and this package reads no secret.

## Installation

The package is internal and is not published. Install it from its directory into the consuming environment:

```bash
uv pip install path/to/model
```

Inside the package directory, `uv sync` creates the package's own isolated environment with its dependencies resolved.

There is nothing to start: `my_model` is an importable library.

## Usage

Construct and validate a complete domain state:

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

Validate data that may be incomplete, and see what is still pending:

```python
from my_model import User, Pending, validate_state, validate_change, InvalidValue

state = validate_state(User, User.initial_data[0])
assert state.pending == {"password", "api_key"}   # awaiting generation
assert not state.is_complete
assert "password" not in state.values             # no placeholder was invented
assert state.values["status"] is True             # default applied

admin = state.resolved(password="generated-1", api_key="generated-2")
assert admin.name == "Admin"

change = validate_change(User, {})
assert change.is_empty                            # omitted fields stay unchanged

change = validate_change(User, {"description": None})
assert change.changes == {"description": None}    # the field permits null

try:
    validate_change(User, {"username": None})     # this one does not
except InvalidValue as invalid:
    assert invalid.fields == ("username",)
else:
    raise AssertionError("expected refusal")
```

Read a Model's logical declarations:

```python
from my_model import Broker, User, TradingPlatform, MODELS, UniqueTogether

spec = Broker.field_spec("user_id")
assert spec.type == "integer" and not spec.nullable

targets = {r.field: r.target for r in Broker.relationships}
assert targets == {"user_id": User, "trading_platform_id": TradingPlatform}

assert UniqueTogether(("user_id", "name")) in Broker.rules

assert len(MODELS) == 14
```

A value that violates a declared field property is refused:

```python
from pydantic import ValidationError
from my_model import Currency

try:
    Currency(name="Bad", code="ABCD")  # code is limited to three characters
except ValidationError:
    pass
else:
    raise AssertionError("expected refusal")
```

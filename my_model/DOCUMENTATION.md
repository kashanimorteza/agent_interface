# my_model

## Purpose and Boundaries

`my_model` is the independent, platform-independent domain Model package for the
Trading Assistant. It defines every domain entity — what it is, which
information belongs to it, how it relates to other entities, which rules
constrain its valid state, and which initial records must logically exist —
as one shared logical source that every other technical component reads
instead of maintaining its own private copy of the same domain meaning.

`my_model` owns:

- domain entity definitions, their fields, and their conceptual relationships;
- validation determinable entirely from one entity's own data;
- declared initial-data records;
- one stable, documented public package interface.

`my_model` does **not** own, and never contains:

- persistence mappings, database tables, columns, foreign keys, indexes, or migrations;
- SQL, ORM sessions, transactions, or repository implementations;
- HTTP routing, request/response contracts, or API transport behaviour;
- business workflows, authorization, or external service calls;
- UI presentation or deployment concerns;
- credential storage, hashing, or encryption strategy — it only declares which
  fields carry credential meaning.

Those responsibilities belong to the Database, Backend, Frontend, and other
technical components, which each derive their own representation from this
package rather than redefining the domain.

## Installation

The package is managed with [uv](https://docs.astral.sh/uv/) and targets
Python 3.13+.

```bash
uv sync
```

A consuming component installs it as a local dependency through its own
ecosystem's local path or workspace mechanism; `my_model` is not published to
a public registry.

## Public Interface

Every domain entity is reachable through exactly one public module, and the
package root re-exports both the modules and the entity types as a
convenience. Both forms are supported; the module-qualified form is
canonical:

```python
# Canonical: module-qualified
import my_model

instance = my_model.user.User(
    name="Ada",
    username="ada",
    password="change-me",
    api_key="change-me",
)

# Alternate: explicit module import
from my_model import user

same_kind_of_instance = user.User(
    name="Grace",
    username="grace",
    password="change-me",
    api_key="change-me",
)
```

A Model is always identified by an imported module, type, or instance —
never by a string name or a registry lookup.

### Public modules

| Module | Type | Represents |
| --- | --- | --- |
| `user` | `User` | An independent user of the system. |
| `trading_platform` | `TradingPlatform` | A supported trading API standard. |
| `instance` | `Instance` | A user-owned connection to a Trading Platform. |
| `currency` | `Currency` | A currency usable by the system. |
| `broker` | `Broker` | A broker owned by a user. |
| `asset` | `Asset` | A tradable asset provided by a broker. |
| `account_group` | `AccountGroup` | A grouping of trading accounts. |
| `account` | `Account` | A funded trading account. |
| `trailing_group` | `TrailingGroup` | A group of trailing rules. |
| `trailing_rule` | `TrailingRule` | One trailing activation and adjustment rule. |
| `partial_group` | `PartialGroup` | A group of partial-close rules. |
| `partial_rule` | `PartialRule` | One partial-close activation and volume rule. |
| `action_group` | `ActionGroup` | A risk-profile grouping of actions. |
| `action` | `Action` | How a position must be opened. |
| `position` | `Position` | The record of an opened or pending position. |

Every entity inherits from `my_model.BaseModel`, which fixes the package-wide
Pydantic configuration: unknown fields are rejected, and assignment is
re-validated. No entity uses `BaseModel` (the shared base class name) as its
own domain name.

## Dependencies

`my_model` depends only on `pydantic` (2.x). It has no dependency on a
database driver, ORM, or API framework — see Model Preferences under
`integrations` for the explicit statement that none is selected for this
package.

## Configuration

`my_model` has no runtime configuration of its own; every entity's shape is
fixed at import time by its class definition. There are no secrets, no
environment variables, and no connection settings to configure.

## Validation, Serialization, and Credential Handling

- **Validation** — each entity validates the rules determinable entirely
  from its own fields (required values, non-blank strings, non-negative
  counts, positive multipliers, and similar single-instance constraints).
  A rule that requires comparing against *other* persisted records — such as
  a uniqueness constraint across a table — is a Database-level concern and is
  declared in the entity's own docstring rather than enforced here, because a
  Model instance has no visibility into other instances and must remain free
  of database queries.
- **Omitted vs. explicit `None` vs. supplied vs. generated** — an optional
  field left out of the input keeps its declared default; explicitly passing
  `None` sets it to `None` when the field permits that; a supplied value
  always wins over a default. A field such as `id` that is generated at
  persistence time is represented as `None` until it has been assigned,
  distinguishing "not yet generated" from "supplied."
- **Partial updates** — `model_copy(update={...})` preserves this same
  distinction: a key left out of `update` leaves the current value
  unchanged, while a key explicitly set to `None` attempts to set the field
  to `None`.
- **Serialization** — every entity uses the standard `model_dump()` and
  `model_dump_json()` operations and produces deterministic output with no
  I/O or side effects.
- **Schema** — every entity uses the standard `model_json_schema()`
  operation to produce its JSON Schema.
- **Credential fields** — an entity that carries a credential or otherwise
  sensitive field declares the field names on its `credential_fields` class
  attribute (for example, `User.credential_fields == {"password", "api_key"}`).
  This only declares sensitive *meaning*; hashing, encryption, and transport
  masking are decided by the components that store or expose the value.
- **Declared initial data** — an entity that requires initial records
  declares them on its `initial_data` class attribute as plain field
  dictionaries. A credential value that must never be a literal is
  represented by the `my_model.GENERATE_SECURELY` sentinel instead of a
  fake placeholder; the component that performs insertion is responsible
  for generating the real value.

## Usage Examples

### Construct a valid instance and observe a validation failure

```python
import my_model
from pydantic import ValidationError

platform = my_model.trading_platform.TradingPlatform(name="Example Platform", code="example")

try:
    my_model.trading_platform.TradingPlatform(name="Example Platform", code="")
except ValidationError as error:
    print("rejected:", error.error_count(), "issue(s)")
```

### Serialize and generate a schema

```python
data = platform.model_dump()
json_text = platform.model_dump_json()
schema = my_model.TradingPlatform.model_json_schema()
```

### Distinguish omitted, explicit `None`, supplied, and generated values

```python
connection = my_model.instance.Instance(user_id=1, name="Primary", trading_platform_id=1)
assert connection.id is None  # waiting for declared generation
assert connection.ip is None  # not supplied; default applies

with_ip = my_model.instance.Instance(user_id=1, name="Primary", trading_platform_id=1, ip=None)
assert with_ip.ip is None  # explicitly supplied as null
```

### Perform a partial update

```python
updated = connection.model_copy(update={"ip": "203.0.113.10"})
untouched = connection.model_copy(update={})
assert untouched.ip is None
assert updated.ip == "203.0.113.10"
```

### Use a declared relationship

```python
owner = my_model.user.User(name="Ada", username="ada", password="change-me", api_key="change-me")
connection = my_model.instance.Instance(
    user_id=1,  # references the owning User's identity
    name="Primary",
    trading_platform_id=platform.id or 1,
)
```

### Handle a credential field without exposing it

```python
assert "password" in my_model.User.credential_fields
safe_view = owner.model_dump(exclude=my_model.User.credential_fields)
assert "password" not in safe_view
```

### Read declared initial data

```python
for record in my_model.User.initial_data:
    # a GENERATE_SECURELY value must be generated by whoever performs insertion,
    # never read or written as a literal credential
    assert record["password"] is my_model.GENERATE_SECURELY
```

# Model

The independent, platform-independent domain Model package. It defines what
the project's domain data *means* — entities, fields, relationships, and
rules — as one shared, reusable source of truth for every other technical
component.

## What this package owns

- Domain entities and value objects, expressed as strict, validated types.
- Field semantics: meaning, optionality, nullability, defaults, and
  credential/sensitive markers.
- Conceptual relationships between entities (cardinality and role).
- Domain rules determinable from a single entity's own data.
- Declarations of required initial data (not its insertion).
- One stable, documented, canonical public import interface.

## What this package does not own

- Persistence: tables, columns, foreign keys, indexes, migrations, ORM
  mappings, or database queries. That belongs to the Database component.
- Transport: HTTP routes, request/response contracts, status codes, or
  authentication workflows. That belongs to the Backend/API component.
- Presentation: UI rendering or user interaction. That belongs to Frontend.
- Cross-record rules such as uniqueness across stored rows, or the existence
  of a referenced record — these require seeing other stored data, which a
  single Model instance cannot do. They are documented here as domain rules,
  and *enforced* by Database.
- Deployment or runtime orchestration.

## Installation and import

This package is managed with [uv](https://docs.astral.sh/uv/) and targets
Python 3.13+.

```bash
uv sync
```

## Public interface and usage pattern

The canonical way to reach a domain Model is **module-qualified** — a
Model's identity is always an imported module, Model type, or Model
instance, never a string name resolved through a registry:

```python
from decimal import Decimal

import my_model

record = my_model.entity.Entity(name="Example", owner_id=1, weight=Decimal("50"), secret="local-only")
```

An equivalent explicit module import is also supported:

```python
from decimal import Decimal

from my_model import entity

record = entity.Entity(name="Example", owner_id=1, weight=Decimal("50"), secret="local-only")
```

Every real domain Model in this package also has a flat package-root
re-export as a convenience, but it does not replace the module-qualified
interface above.

Every concrete Model in this package extends one shared project base class
named `BaseModel` (in this package's internal `_base` module) — never a
class named `Model`, which is reserved for the Model Component concept
itself.

## Model categories

- **Entities** — independent domain concepts with their own identity (most
  types in this package), e.g. a user, a grouping, or a configured item.
  Every entity's `id` field is generated (defaults to `None` until
  persisted) — never invented as a placeholder by this package.
- **Reusable domain types** — a shared constrained type used by more than
  one field, defined once instead of repeating the same constraint. This
  package currently declares one: a percentage value shared by every rule
  that expresses a percentage.
- Relationships between entities are expressed as plain `*_id` integer
  references (not embedded objects), so entities remain independently
  constructible and importable in any order.
- This package does not currently declare a domain `Enum` or an independent
  compound Value Object, because no field in the current domain represents
  a fixed, closed set of values or an independent value with its own rules
  beyond a single constrained primitive. Both categories are supported by
  this package's foundation and would be added the same way as the
  reusable type below, the moment a field needs one.
- `my_model.entity.Entity` is a domain-neutral example Model shipped only
  to keep the usage examples below runnable. It is not part of the
  project's domain Model set.

## Boundary with other Components

| Concern | Owner |
| --- | --- |
| Domain meaning, fields, relationships, single-record validation | **Model** (this package) |
| Tables, migrations, cross-record uniqueness, referenced-record existence | Database |
| HTTP endpoints, request/response shaping, auth | Backend / API |
| Rendering and interaction | Frontend |

## Validation, serialization, credential, and extension rules

- Every Model extends the shared strict base (`extra="forbid"`): an unknown
  field is a validation error, not a silently ignored value.
- Validation covers only what one instance's own data can determine (field
  types, per-field constraints, and same-instance cross-field checks).
  Rules that depend on other stored records (uniqueness, referenced-record
  existence) are documented in the owning class's docstring and enforced by
  Database.
- Serialization uses the modern Pydantic v2 API only: `model_dump`,
  `model_dump_json`, `model_json_schema`, `model_validate`, `model_copy`.
  Legacy v1 APIs (`.dict()`, `.json()`, `parse_obj()`) are not used.
- A field marked as a credential documents its required storage-at-rest
  treatment; this package never stores, hashes, encrypts, or transmits the
  raw value.
- A required initial-data declaration that needs a securely generated
  credential uses a sentinel (`GENERATE_SECURELY`) instead of a fake
  placeholder value; the generation itself happens outside this package.
- Extending this package with a new domain type means adding one new module
  that extends the shared base and importing it from the package root — it
  does not require changing any existing type.

## Complete usage examples

Every example below is domain-neutral, runnable as written against this
package's `my_model.entity.Entity` example fixture, and uses only imported
modules, Model types, or Model instances — never a string-based lookup, an
internal module, or an ORM/Database/API detail. Every example is executed
as part of this package's own test suite.

### 1. Import the package namespace and use its module-qualified interface

```python
from decimal import Decimal

import my_model

record = my_model.entity.Entity(name="Example", owner_id=1, weight=Decimal("50"), secret="local-only")
assert record.name == "Example"
```

### 2. Import one public Model module directly

```python
from decimal import Decimal

from my_model import entity

record = entity.Entity(name="Example", owner_id=1, weight=Decimal("50"), secret="local-only")
assert record.name == "Example"
```

### 3. Construct a valid Model instance

```python
from decimal import Decimal

import my_model

record = my_model.entity.Entity(name="Example", owner_id=1, weight=Decimal("50"), secret="local-only")
assert record.name == "Example"
```

### 4. Observe and handle a validation failure

```python
from decimal import Decimal

import my_model
from pydantic import ValidationError

try:
    my_model.entity.Entity(
        name="Example",
        owner_id=1,
        weight=Decimal("50"),
        secret="local-only",
        unexpected_field="not allowed",
    )
    handled = False
except ValidationError as error:
    handled = error.error_count() > 0
assert handled
```

### 5. Serialize an instance to a dict and to JSON

```python
from decimal import Decimal

import my_model

record = my_model.entity.Entity(name="Example", owner_id=1, weight=Decimal("50"), secret="local-only")
as_dict = record.model_dump()
as_json = record.model_dump_json()
assert as_dict["name"] == "Example"
assert '"name":"Example"' in as_json.replace(" ", "")
```

### 6. Generate a Model's JSON Schema

```python
import my_model

schema = my_model.entity.Entity.model_json_schema()
assert "name" in schema["properties"]
```

### 7. Distinguish omitted, explicit-null, supplied, default, and generated values

```python
from decimal import Decimal

import my_model

# `status` is omitted here, so its declared default applies.
record = my_model.entity.Entity(name="Example", owner_id=1, weight=Decimal("50"), secret="local-only")
assert record.status is True  # default, not because it was supplied

# `description` is explicitly supplied as null and is preserved as None.
described = my_model.entity.Entity(
    name="Example", owner_id=1, weight=Decimal("50"), secret="local-only", description=None
)
assert described.description is None

# `name` was supplied with a value above, replacing no prior state.
assert record.name == "Example"

# `id` is left unset: it is a generated identity, not yet assigned.
assert record.id is None
```

### 8. Perform a partial update that preserves the documented update semantics

```python
from decimal import Decimal

import my_model

record = my_model.entity.Entity(
    name="Example", owner_id=1, weight=Decimal("50"), secret="local-only", description="Original"
)

# Omitting a field from the update leaves its current value unchanged.
renamed = record.model_copy(update={"name": "Renamed"})
assert renamed.description == "Original"

# Explicitly setting a field to null attempts to null it (valid only if the
# Model permits null for that field).
cleared = record.model_copy(update={"description": None})
assert cleared.description is None
```

### 9. Use a reusable type and a declared relationship

```python
from decimal import Decimal

import my_model

# Reusable type: `weight` uses the same `Percentage` type this package shares
# across every field that expresses a percentage, instead of repeating the
# same 0-100 bound on each one.
# Declared relationship: `owner_id` identifies the other entity this one
# conceptually belongs to.
record = my_model.entity.Entity(name="Example", owner_id=1, weight=Decimal("50"), secret="local-only")
assert record.owner_id == 1
assert Decimal("0") <= record.weight <= Decimal("100")
```

### 10. Handle a sensitive or credential field without exposing its protected value

```python
from decimal import Decimal

import my_model

record = my_model.entity.Entity(name="Example", owner_id=1, weight=Decimal("50"), secret="local-only")

field_info = my_model.entity.Entity.model_fields["secret"]
assert field_info.json_schema_extra == {"credential": True, "storage_at_rest": "hash"}

# This package never hashes, masks, or transmits the raw value; a consumer
# that displays or logs a record excludes it explicitly.
dumped = record.model_dump(exclude={"secret"})
assert "secret" not in dumped
```

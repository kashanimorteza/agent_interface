# my_model

The shared, platform-independent logical Model package for the Trading Assistant Target.

## Purpose and boundaries

`my_model` gives every other component of the Trading Assistant one shared logical
understanding of its domain data: what each entity is, which information belongs to
it, how it relates to other entities, which single-record rules constrain its valid
state, and which initial records must logically exist.

`my_model` is **not** a database layer, an API layer, a business workflow layer, a
UI layer, or a deployment layer. It never:

- maps to database tables, columns, or ORM constructs;
- executes a database query or opens a session;
- performs an HTTP request or defines transport-specific request/response shapes;
- calls an external service, sends a message, or performs any other I/O; or
- enforces a rule that requires querying persisted state (for example, that a
  combination of fields is unique across records — that belongs to Database).

Technical layers (Database, Backend, Frontend) derive their own representations from
`my_model`, but `my_model` remains the one authoritative definition of what each
entity means.

## Installation

`my_model` is an internal, independently installable package managed with `uv`:

```bash
cd my_model
uv sync
```

A consuming component adds it as a local dependency through its own package
manager's local path or workspace mechanism; it is not published to a public
registry.

## Public interface and usage pattern

The canonical way to use the package is a module-qualified import:

```python
import my_model

user = my_model.user.User(id=1, name="Admin", username="admin", password="x", api_key="y")
```

An equivalent, explicit alternative imports one public submodule directly:

```python
from my_model import user

instance = user.User(id=1, name="Admin", username="admin", password="x", api_key="y")
```

Every public Model type is also re-exported from the package root as a convenience
(for example, `my_model.User`), but this never replaces the module-qualified
interface above as the canonical usage pattern. A Model is always identified by an
imported module, type, or instance — never by a string name or a registry lookup.

Internal modules (any module whose name starts with `_`, such as `my_model._base`'s
`credential_field` helper) are implementation details and are not a public contract.

## Categories

Every Model in this package is an **Entity Model**: it represents one meaningful,
independently identifiable domain concept with its own logical identity. This
package currently defines no Value Object, Enum, Root Model, or Generic Model,
because no field in the current Target needs one of those categories to be
represented correctly.

The package currently defines fifteen domain entities, organized here by the
responsibility they share:

| Area | Entities |
| --- | --- |
| Identity and platform access | `User`, `TradingPlatform` |
| Platform connectivity | `Instance` |
| Financial reference data | `Currency`, `Broker`, `Asset` |
| Trading accounts | `AccountGroup`, `Account` |
| Risk management rules | `TrailingGroup`, `TrailingRule`, `PartialGroup`, `PartialRule` |
| Actions and positions | `ActionGroup`, `Action`, `Position` |

A relationship between two entities is represented as a plain integer field named
`<role>_id` (for example, `Instance.user_id` identifies the owning `User`). The
field's presence and nullability state the relationship's cardinality and whether
it is optional; `my_model` does not embed a nested object for a relationship,
because resolving the referenced record is a persistence concern owned by Database.

## Boundary with other Components

- **Database** maps each entity to persistent storage, enforces every rule that
  requires reading other persisted records (including cross-record uniqueness),
  applies the storage strategy a declared credential field requires, and supplies
  every system-generated value (a primary identity or a generated credential) that
  this package intentionally leaves out of its initial-data declarations.
- **Backend** derives request- and response-shaped representations from these
  entities and enforces rules that need actor, permission, or workflow context.
- **Frontend** presents data derived from what Backend publishes.

`my_model` itself never performs I/O and never depends on Database, Backend, or
Frontend.

## Validation, serialization, and credential rules

- Every entity rejects an unknown field (`extra="forbid"`): an unexpected field
  usually means a typo or a stale caller, not extensible data.
- A validation failure raises `pydantic.ValidationError`; construction never
  silently drops or coerces a value that would hide invalid domain data.
- A field's default is applied only when the field is omitted. An explicit value —
  including an explicit `False`, `0`, or `None` on a field that permits it — is
  never overridden by a default.
- A financial field (money, percentage, or volume) uses `Decimal` for exact
  precision; `Asset.point_size` explicitly uses `float`, matching a physical
  measurement rather than a monetary amount, exactly as the Target declares.
- A credential field (for example `User.password`) is declared through the
  package's shared `credential_field` helper, which records that the field is a
  credential and which storage strategy Database must apply, in the field's
  `json_schema_extra`:  `{"credential": True, "storage_at_rest": "hash" | "encrypted"}`.
  `my_model` never decides how a credential is hashed, encrypted, or otherwise
  protected — only that it must be.
- Every entity supports `model_dump()`, `model_dump_json()`, and
  `model_json_schema()` for deterministic, side-effect-free serialization and
  schema generation.
- Where an entity declares initial data (see `<module>.INITIAL_DATA`), the
  declaration is a list of plain dictionaries rather than constructed instances,
  because a system-generated field (a primary identity, or a credential requiring
  secure generation) is intentionally absent until Database supplies it.

## Usage examples

Construct a valid instance:

```python
import my_model

currency = my_model.Currency(id=1, user_id=1, code="USD", symbol="$")
```

Observe a validation failure for invalid data:

```python
from pydantic import ValidationError

try:
    my_model.Currency(id=1, user_id=1, code="US")  # code must be exactly 3 characters
except ValidationError as error:
    print(error)
```

Serialize an instance and generate its schema:

```python
payload = currency.model_dump()
json_text = currency.model_dump_json()
schema = my_model.Currency.model_json_schema()
```

Distinguish omitted values, explicit `None`, supplied values, and defaults:

```python
broker_a = my_model.Broker(id=1, name="FxPro", user_id=1)              # description omitted
broker_b = my_model.Broker(id=1, name="FxPro", user_id=1, description=None)  # description explicit None
assert broker_a == broker_b  # both leave description unset, at its default of None

asset = my_model.Asset(
    id=1, broker_id=1, symbol="EUR/USD", category="Currency", status=False,
)
assert asset.status is False  # an explicit False is never overridden by the field's default
```

Perform a partial update while preserving update semantics:

```python
from decimal import Decimal

rule = my_model.TrailingRule(
    id=1,
    name="Trigger 50%",
    trailing_group_id=1,
    trigger_percentage=Decimal("50"),
    take_profit_adjustment=Decimal("1"),
)
updated = rule.model_copy(update={"stop_loss_adjustment": Decimal("2")})
assert updated.take_profit_adjustment == Decimal("1")  # omitted from the update: unchanged
assert updated.stop_loss_adjustment == Decimal("2")    # supplied in the update: replaced
```

Handle a credential field without exposing its protected value:

```python
user = my_model.User(id=1, name="Admin", username="admin", password="x", api_key="y")
password_field = my_model.User.model_fields["password"]
assert password_field.json_schema_extra == {"credential": True, "storage_at_rest": "hash"}
# my_model declares the credential and its required storage strategy; it never
# hashes, encrypts, or otherwise transforms the value itself.
```

A declared relationship is a plain identifying field:

```python
instance = my_model.Instance(id=1, user_id=1, name="MetaTrader", trading_platform_id=1)
assert instance.user_id == 1            # the User this Instance belongs to
assert instance.trading_platform_id == 1  # the Trading Platform this Instance uses
```

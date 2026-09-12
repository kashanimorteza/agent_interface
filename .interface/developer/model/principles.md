# Model Standard

> **Authoritative Standard for the Model Component**
>
> This document is the single source of truth for the project's Model component.
>
> Every AI agent, developer, reviewer, or automation that creates, changes, validates, or reasons about Model code MUST read and follow this document before making changes.
>
> **Principles override preferences, framework defaults, convenience, and implementation choices.**
>
> A project may add stricter rules, but it must not weaken the rules defined here.

---

# 1. Purpose

Model is an independent shared application component that defines the domain entities, concepts, fields, relationships, and rules from which the project is formed.

Model gives every technical component one shared logical understanding of the project's data.

Model is responsible for describing:

- what each domain entity or concept is,
- which information belongs to it,
- how it relates to other Models,
- which rules constrain its valid state,
- which initial records are logically required,
- and how those domain definitions are exposed as one reusable package.

Model is **not** a database layer, API layer, business workflow layer, UI layer, or deployment layer.

---

# Project Independence

This Standard is reusable across Targets. It defines how a Model Component works, not which domain a particular project contains.

The following belong only to the current Target's authoritative definition and MUST NOT be copied into this Standard:

- domain-specific Model names,
- domain-specific field names or values,
- project relationships and uniqueness rules,
- project Initial Data,
- project phases, workflows, integrations, or platform names,
- examples that reveal the current Target's domain.

Examples in this Standard use neutral placeholders only. When an implementation needs the actual Model set, fields, relationships, or Initial Data, it reads the current Target definition and applies this Standard to those sources. Changing the Target MUST NOT require changing this Standard.

---

# Architectural Foundation

This Standard is aligned with the separation described by OMG Model Driven Architecture (MDA): a platform-independent model expresses domain meaning, while platform-specific models and implementations realize that meaning for particular technologies.

Within this Standard:

- the logical Model is the platform-independent domain representation;
- Database, API, Backend, Frontend, and integration representations are platform-specific derivations;
- a derivation preserves the identity and meaning of the logical Model while adding only the concerns of its own platform;
- a transformation from the logical Model to a technical representation may be manual, generated, or tool-assisted, but it must remain traceable.

UML may be used as a formal notation for structural and behavioural modeling. ISO/IEC/IEEE 42010 may be used for architecture-description vocabulary such as viewpoints, model kinds, and architecture descriptions. These references guide the organization and communication of the architecture; they do not prescribe Python, Pydantic, a file format, a modeling tool, or a code-generation process.

This is a project Model Standard aligned with those ideas. It does not claim full conformance to MDA, UML, ISO/IEC/IEEE 42010, or any other external standard. External standards remain references; the rules in this document govern the Model implementation when they are applicable.

---

# Authority by Concern

Different sources are authoritative for different decisions:

| Concern | Authoritative source |
| --- | --- |
| Domain Model names, fields, relationships, domain rules, and Initial Data | Current Target Model definition |
| Model boundaries, validation ownership, representation independence, and public package contract | This Model Standard |
| Python version, Pydantic version, defaults, and compatible implementation choices | Model Preferences |
| Framework syntax and version-specific behaviour | Current Pydantic documentation and the installed compatible toolchain |
| Architecture vocabulary and optional modeling notation | Referenced external standards |

An external standard never silently adds a Target Model, field, relationship, rule, or Initial Data record. A framework default never overrides an explicit Target definition or this Standard. When sources govern different concerns, apply each source only within its authority and record a consequential implementation choice where the governing source requires it.

---

# 2. Core Principles

## 2.1 Model represents domain entities and concepts

**MUST:** Each Model represents one meaningful entity or concept in the project domain.

A Model defines:

- its logical identity,
- its fields,
- its relationships,
- its valid state,
- and its domain meaning.

**NEVER:** Define a Model merely because there is:

- a database table,
- an API endpoint,
- a web form,
- a page,
- a framework class,
- or a transport payload.

The domain defines the Model.

Technical components derive their own representations from the Model.

---

## 2.2 Model is an independent shared package

The resolved Model set MUST be implemented as one independent package.

The Model package MUST provide one documented public import interface made of explicit public submodules and typed Model classes. The canonical consumer style is module-qualified import, so a consumer can use `import model` followed by `model.<module>.<ModelType>`, or `from model import <module>` followed by `<module>.<ModelType>`.

Model identity MUST be represented by an imported module, Model type, or Model instance. A public Model operation MUST NOT require a Model name encoded as a string, an untyped string registry lookup, or dynamic attribute resolution from caller-controlled text. String values remain valid only as ordinary domain data when the Model definition explicitly declares a string field.

Every public Model MUST be exposed exactly once through that interface.

Compatible application components MUST import the shared Model package instead of maintaining private copies of the same domain definitions.

Canonical examples:

```python
import model

record = model.entity.Entity(name="Example")
payload = record.model_dump()
schema = model.entity.Entity.model_json_schema()
```

An equivalent explicit module import is also supported:

```python
from model import entity

record = entity.Entity(name="Example")
```

rather than:

```python
from backend.models import Entity
from database.models import Entity
from frontend_contracts import Entity
```

when all three are attempting to redefine the same logical Model.

A consumer that cannot import the package directly MAY use a representation derived from the same Model definitions through its own declared boundary.

---

## 2.3 Model is the logical source between technical components

Model is the shared logical source for domain data.

Technical components MAY derive representations suitable for their own responsibilities.

Examples:

```text
Model
 ├── Database representation
 ├── Backend/API representation
 ├── Frontend representation
 └── External integration representation
```

Every derived representation MUST preserve the meaning of the Model fields and relationships it includes.

A technical representation MAY contain only a subset of Model fields.

Examples:

- create input,
- partial update,
- public output,
- internal output,
- database persistence representation.

Omitting a field from a representation does not remove that field from the Model and does not weaken the rules governing a complete domain state.

---

# 3. Model Boundaries

Model owns:

- domain representations,
- field semantics,
- conceptual relationships,
- domain rules,
- validation determinable from the Model's own data,
- initial-data declarations,
- reusable domain enums,
- reusable domain value objects,
- shared domain types,
- deterministic derived values,
- one stable public package interface.

Model does **not** own:

- persistence mappings,
- SQLAlchemy ORM models,
- database tables,
- columns,
- foreign keys,
- indexes,
- SQL constraints,
- database queries,
- repository implementations,
- transaction handling,
- migrations,
- Alembic,
- FastAPI routers,
- HTTP request/response contracts,
- HTTP status codes,
- API transport behavior,
- authentication workflows,
- application services,
- external API calls,
- email sending,
- message publishing,
- UI presentation,
- deployment.

These belong to their respective technical components.

---

# 4. Technology Standard

The default implementation technology for Model is:

```text
Python        3.13+
Pydantic      v2
Typing        modern Python typing
Enums         StrEnum
Precision     Decimal where exact decimal semantics matter
Time          timezone-aware domain semantics
```

Pydantic is the default implementation tool for Model because it provides:

- strong typing,
- validation,
- serialization,
- reusable domain objects,
- schema introspection,
- deterministic transformation,
- and clean composition.

Pydantic MUST NOT change the architectural meaning of Model.

Framework behavior is subordinate to Model Principles.

---

# 5. Model Categories

A Model package MAY contain different categories of domain definitions.

## 5.1 Entity Model

Represents one meaningful domain entity.

Example:

```python
class Entity(Model):
    ...
```

## 5.2 Value Object

Represents a domain value with meaning and rules.

Examples:

```text
Money
Price
CodeValue
Percentage
TimeRange
EmailAddress
Identifier
```

## 5.3 Enum

Represents a stable reusable set of domain values.

## 5.4 Root Model

Represents one logical root value when that value itself is the domain concept.

## 5.5 Generic Model

Represents a truly reusable typed domain structure.

Do not create categories merely for architectural appearance.

---

# 6. Field Standard

A field represents one logical piece of information carried by a Model.

A field MAY define, where applicable:

- logical type,
- meaning,
- identity role,
- uniqueness meaning,
- optionality,
- nullability,
- default behavior,
- generation behavior,
- credential/sensitive nature,
- domain constraints.

Field definitions MUST remain independent of:

- database column types,
- SQLAlchemy mappings,
- transport formats,
- API framework declarations,
- UI controls.

---

# 7. Required, Optional, Null, and Generated Values

The following states MUST remain distinct:

```text
not supplied
explicitly null
supplied with a value
waiting for declared generation/default
```

These are different domain states.

Example:

```python
name: str
nickname: str | None
```

does not mean the same thing as:

```python
nickname: str | None = None
```

A required field does not necessarily need to be supplied by the caller if the operation permits omission and a declared default or generation mechanism supplies it before the resulting state is considered complete.

**NEVER:** Insert fake placeholder values merely to satisfy a required field.

---

# 8. Partial Update Semantics

Partial updates MUST preserve the distinction between omission and explicit null.

```text
field omitted
    → leave current value unchanged

field explicitly set to null
    → attempt to set value to null

field supplied with value
    → attempt to replace current value
```

Explicit null is valid only if the Model permits null for that field.

A partial representation is not automatically a complete domain state.

---

# 9. Defaults

Defaults complete unspecified properties.

An explicitly declared Model property always wins over a default.

This includes explicit:

```text
false
0
empty string
null
```

when those values are valid and intentionally declared.

Defaults MUST be applied property-by-property.

A default MUST NOT:

- silently override an explicit Model declaration,
- introduce a new field merely because its name matches a convention,
- invent a relationship,
- change the logical meaning of a field.

---

# 10. Pydantic v2 Base Standard

Use Pydantic v2 only.

Recommended base:

```python
from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
```

Shared configuration MAY be placed in a common Model base when it represents a project-wide Model rule.

Avoid deep inheritance hierarchies.

Prefer composition.

---

# 11. Modern Pydantic v2 API

Use:

```python
Model.model_validate(...)
instance.model_dump()
instance.model_dump_json()
instance.model_copy()
```

Do not introduce legacy Pydantic v1 APIs such as:

```python
parse_obj()
.dict()
.json()
.copy()
```

Do not use:

```python
class Config:
    ...
```

for new Pydantic models.

Use:

```python
model_config = ConfigDict(...)
```

---

# 12. Naming

Model names MUST represent domain meaning.

Good:

```text
Entity
Operation
Record
Resource
Event
Price
Money
OperationKind
CodeValue
```

Avoid framework-oriented names such as:

```text
EntitySchema
EntityDTO
EntityRequest
EntityResponse
EntityTable
EntityOrm
```

inside the independent Model package unless the domain itself genuinely uses that concept.

Transport-specific or persistence-specific names belong to their own components.

---

# 13. Validation Ownership

Validation MUST be enforced by the component that has the information required to evaluate it.

## Model validation

Model validates rules determinable entirely from its own data.

Examples:

```text
price > 0
start <= end
symbol is not empty
high >= low
percentage is between allowed bounds
```

## Backend Logic validation

Backend Logic enforces rules that require:

- operation context,
- actor context,
- permissions,
- workflow state,
- external state.

Example:

```text
Is this actor allowed to perform this operation?
```

## Database validation

Database guarantees rules requiring persisted state.

Examples:

```text
email is unique across records
referenced entity exists
persistent relationship remains valid
```

The rule remains logically traceable to the Model even when another component is responsible for enforcement.

---

# 14. Field Validation

Prefer declarative validation first.

Use:

- `Annotated`,
- `Field`,
- reusable value objects,
- enums,
- constrained domain types.

Example:

```python
from typing import Annotated
from pydantic import Field


NonEmptyName = Annotated[
    str,
    Field(min_length=1, max_length=100),
]
```

Use `field_validator` when field-specific logic cannot be expressed cleanly through declarative constraints.

Example:

```python
from pydantic import field_validator


class Resource(Model):
    code: str

    @field_validator("code")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        value = value.strip().upper()

        if not value:
            raise ValueError("symbol cannot be empty")

        return value
```

---

# 15. Cross-Field Validation

Use `model_validator` when a domain rule depends on multiple fields.

Example:

```python
from pydantic import model_validator


class PriceRange(Model):
    low: Decimal
    high: Decimal

    @model_validator(mode="after")
    def validate_range(self):
        if self.high < self.low:
            raise ValueError("high must be greater than or equal to low")

        return self
```

Validators MUST NOT:

- query a database,
- call external services,
- send messages,
- mutate unrelated state,
- orchestrate business workflows.

---

# 16. Strict Validation

Use strict validation when implicit type coercion could hide invalid domain data.

Example:

```python
class Quantity(Model):
    model_config = ConfigDict(strict=True)

    value: int
```

Strict mode SHOULD be enabled deliberately, not mechanically for every Model.

The decision depends on domain semantics.

---

# 17. Reusable Domain Types

When the same validation or meaning appears repeatedly, create one reusable domain type.

Examples:

```text
EntityId
OperationId
CodeValue
PositivePrice
Percentage
CategoryCode
```

Prefer reusable domain types over duplicated validators.

---

# 18. StrEnum

Use `StrEnum` for stable reusable domain values.

Example:

```python
from enum import StrEnum


class OperationKind(StrEnum):
    FIRST = "first"
    SECOND = "second"
```

Prefer:

```python
OperationKind.FIRST
```

over repeated magic strings.

Enums belong to Model only when they represent domain meaning.

Database storage strategy for the enum belongs to Database.

API representation belongs to API.

---

# 19. Literal

Use `Literal` for a small local closed set when a reusable named enum would add no value.

Example:

```python
from typing import Literal


SortDirection = Literal["asc", "desc"]
```

If the value has reusable domain identity, prefer `StrEnum`.

---

# 20. Value Objects

Use a dedicated Model when a primitive value has independent domain meaning or rules.

Example:

```python
from decimal import Decimal


class Price(Model):
    value: Decimal
```

A value object SHOULD be:

- small,
- focused,
- strongly typed,
- deterministic,
- free from unrelated side effects.

---

# 21. Financial Values

Use `Decimal` where exact decimal semantics matter.

Examples:

```text
price
money
amount
balance
commission
exchange rate
quantity when decimal precision matters
```

Do not use `float` blindly for financial domain values.

Example:

```python
from decimal import Decimal


class Price(Model):
    value: Decimal
```

Rounding rules belong to Model only when rounding is itself a domain rule.

Database precision/scale belongs to Database.

---

# 22. Time Semantics

Model MUST distinguish:

```text
instant in time
local wall-clock time
timezone rule
duration
date
```

Use timezone-aware datetime values for real-world instants.

UTC is the preferred canonical representation for absolute instants.

Do not mix naive and timezone-aware datetime values without an explicit domain reason.

Example:

```python
from datetime import datetime


class Trade(Model):
    executed_at: datetime
```

If the domain concept is:

```text
09:30 America/New_York
```

do not reduce it permanently to one UTC time if the timezone rule itself is part of the domain meaning.

Persistence strategy belongs to Database.

---

# 23. RootModel

Use `RootModel` only when the domain concept genuinely represents one root value.

Example:

```python
from pydantic import RootModel


class Symbols(RootModel[list[str]]):
    pass
```

Do not use `RootModel` when named fields would express meaning more clearly.

---

# 24. Generic Models

Use generic Models only for genuinely reusable domain structures.

Example:

```python
from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class Collection(Model, Generic[T]):
    items: list[T]
```

Do not introduce generics for a single isolated use case.

---

# 25. Discriminated Unions

Use discriminated unions when one domain concept has multiple explicit variants.

Example:

```python
from typing import Annotated, Literal
from pydantic import Field


class VariantA(Model):
    type: Literal["variant_a"]


class VariantB(Model):
    type: Literal["variant_b"]
    value: Decimal


DomainVariant = Annotated[
    VariantA | VariantB,
    Field(discriminator="type"),
]
```

Prefer discriminated unions over manual type switching when the variants are part of the domain.

---

# 26. Serialization

Serialization in Model MUST be:

- deterministic,
- side-effect free,
- domain-oriented.

Use `field_serializer` for field-level serialization logic when necessary.

Use `model_serializer` only when whole-model serialization genuinely requires it.

Serializers MUST NOT:

- query storage,
- call external services,
- perform business workflows.

Transport-specific formatting belongs to API or integration layers.

---

# 27. Computed Fields

Use `computed_field` for deterministic values derived entirely from Model data.

Example:

```python
from pydantic import computed_field


class PriceRange(Model):
    high: Decimal
    low: Decimal

    @computed_field
    @property
    def spread(self) -> Decimal:
        return self.high - self.low
```

Computed fields MUST NOT perform I/O.

---

# 28. Aliases

Use aliases only when they represent a real shared interoperability need.

Internal Python naming SHOULD remain idiomatic `snake_case`.

External transport naming conventions SHOULD normally be handled by the relevant technical layer.

Do not make Model depend on one API's JSON naming unless that external naming is itself part of the shared domain contract.

---

# 29. Extra Fields

For strict domain objects, prefer:

```python
model_config = ConfigDict(extra="forbid")
```

Unexpected fields often indicate:

- a typo,
- a stale consumer,
- a contract mismatch.

A different policy MAY be used when the domain explicitly permits extensible data.

The policy must be intentional.

---

# 30. Immutability

Use frozen Models where immutability is part of the domain semantics.

Example:

```python
class CodeValue(Model):
    model_config = ConfigDict(frozen=True)

    value: str
```

Do not make mutable concepts immutable merely for style.

---

# 31. Relationships

Relationships describe conceptual connections between Models.

A relationship MAY specify:

- cardinality,
- optional participation,
- role of each side,
- logical field carrying the relationship.

Examples:

```text
one-to-one
one-to-many
many-to-many
```

If an association has its own domain meaning, it MAY itself be a Model.

Example:

```text
Entity
Role
EntityMembership
```

if `EntityMembership` carries meaningful domain state.

Model MUST NOT define:

- foreign-key implementation,
- SQLAlchemy relationship loading,
- cascade behavior,
- join strategy,
- database referential actions.

Those belong to Database.

---

# 32. Initial Data

Initial data that must logically exist when the project begins is part of Model.

Model declares:

- which initial records must exist,
- their logical identity,
- required domain values.

Model MUST NOT perform their insertion.

Database is responsible for persistence and permitted generated values.

Example:

```text
DomainKind:
- first
- second
```

or:

```text
SystemRole:
- admin
- entity
```

when these are actual domain records rather than implementation constants.

---

# 33. Sensitive and Credential Fields

Model MAY declare that a field is sensitive or credential-related when that property is part of its domain meaning.

Examples:

```text
password
api credential
secret
token
private key reference
```

Model does not decide:

- HTTP exposure,
- storage hashing algorithm,
- database encryption,
- transport masking.

Those belong to responsible technical components.

Consumers MUST preserve the sensitive meaning declared by Model.

---

# 34. Deterministic Domain Behavior

Small deterministic behavior that belongs directly to the data concept MAY live in Model.

Good examples:

```text
normalize symbol
calculate spread
validate range
derive full name
determine local invariant
```

Not Model behavior:

```text
perform operation
charge balance
persist entity
send notification
call external service
authorize request
```

The difference is whether the behavior is determinable from the Model's own data and belongs to the concept itself.

---

# 35. Side-Effect Rule

Model code MUST be free from unrelated side effects.

Model validators, computed fields, serializers, and constructors MUST NOT:

- query Database,
- open sessions,
- write files,
- perform network requests,
- call external APIs,
- send email,
- publish events,
- perform application operations.

---

# 36. Public Package Interface

The Model package MUST expose a stable documented public interface.

Preferred pattern:

```text
model/
├── __init__.py
├── entity.py
├── operation.py
├── resource.py
├── enums/
└── types/
```

Public imports MAY be re-exported from the package root:

```python
from .entity import Entity
from .operation import Operation
from .resource import Resource

__all__ = [
    "Entity",
    "Operation",
    "Resource",
]
```

Consumers MUST import public Model modules or types from the documented package interface instead of deep internal modules. Package-root class re-exports MAY exist as a convenience, but they do not replace the canonical module-qualified interface.

Internal file organization MAY change without breaking the logical public Model interface.

---

# 37. One Definition Rule

Each resolved logical Model MUST have one authoritative definition.

Do not create competing domain definitions such as:

```text
backend.Entity
database.Entity
worker.Entity
frontend.Entity
```

that independently define the same domain identity.

Technical layers MAY derive specialized representations.

They MUST NOT silently redefine domain meaning.

---

# 38. Derived Representations

Technical representations may be narrower than the Model.

Example:

```text
Entity
├── id
├── email
├── password credential
├── status
└── created_at

API Public Entity
├── id
├── email
└── status
```

This is valid.

The API representation is a derived subset.

It does not become the authoritative definition of Entity.

---

# 39. Model Completeness

A representation can be partial while the domain Model remains complete.

Examples:

```text
create input
partial update
search filter
public output
summary view
```

Model rules that apply to the final domain state still remain in force.

Do not weaken a Model rule merely because a technical representation contains fewer fields.

---

# 40. Framework Independence

The logical definition of a Model MUST remain understandable without knowledge of:

- FastAPI,
- SQLAlchemy,
- PostgreSQL,
- React,
- Flutter,
- a specific message broker,
- a specific API format.

Pydantic is the implementation technology.

Pydantic is not the domain itself.

---

# 41. Database Independence

Model MUST NOT contain SQLAlchemy persistence concerns.

The following do not belong in Model Standard:

```text
__tablename__
Mapped
mapped_column
ForeignKey
relationship
index
unique database constraint implementation
selectinload
lazy loading
cascade
N+1 strategy
transaction behavior
session behavior
Alembic migrations
```

These belong to Database Standard.

The Model MAY declare the logical requirement that motivates them.

Example:

```text
Entity.identifier must be unique
```

but Database determines how persistent uniqueness is guaranteed.

---

# 42. API Independence

Model MUST NOT contain FastAPI or HTTP transport concerns.

The following do not belong in Model Standard:

```text
APIRouter
Depends
HTTPException
status_code
Request
Response
query parameter behavior
HTTP headers
response_model
transport-only create/update DTOs
```

These belong to API/Backend Standard.

The API derives representations from Model.

---

# 43. Testing Standard

Model tests SHOULD cover:

- valid state,
- invalid state,
- boundary values,
- nullability,
- defaults,
- omitted vs explicit null semantics,
- enum behavior,
- reusable domain types,
- value objects,
- cross-field validation,
- discriminated unions,
- serialization,
- computed fields,
- immutability,
- deterministic behavior.

Example:

```python
import pytest
from pydantic import ValidationError


def test_price_must_be_positive():
    with pytest.raises(ValidationError):
        Price(value=Decimal("-1"))
```

Tests for persistence constraints belong to Database tests.

Tests for HTTP behavior belong to API tests.

---

# 44. Documentation Standard

The Model Component MUST include a public `README.md` at its package boundary. The README is a required developer-facing explanation of the completed Model package, not an optional project note.

The README MUST explain, in clear language:

- what the Model Component is responsible for and what it does not own;
- how the package is installed and imported;
- the public package interface and the supported usage pattern;
- the Model categories and the meaning of their important fields and relationships;
- the boundary between Model, Database, Backend, API, and other Components;
- the applicable validation, serialization, credential, and extension rules;
- a small set of domain-neutral examples that do not expose project-specific Target information.

The README MUST be generated or updated as part of Model development and MUST be verified for existence, completeness, and consistency with the public interface before the Model Component is reported complete. A Model implementation without this README is incomplete.

Important Models SHOULD communicate meaning through:

- clear Model names,
- clear field names,
- precise types,
- focused descriptions where necessary.

Avoid comments that merely repeat code.

Document domain meaning and non-obvious invariants.

---

# 45. Forbidden Legacy Pydantic Patterns

Do not introduce:

```text
Pydantic v1 APIs
class Config:
orm_mode = True
parse_obj()
.dict()
.json()
.copy()
BaseSettings from pydantic
```

`BaseSettings` belongs to application configuration, not Model.

---

# 46. Forbidden Architecture Patterns

Model MUST NOT:

- become an ORM layer,
- contain SQLAlchemy mappings,
- become an API transport layer,
- contain FastAPI-specific code,
- execute database queries,
- manage sessions,
- perform transactions,
- implement repositories,
- implement service workflows,
- call external services,
- duplicate domain definitions per technical layer,
- use framework objects as domain identity,
- use `dict[str, Any]` as a universal substitute for modeling,
- introduce deep inheritance without domain justification,
- hide I/O inside properties,
- perform side effects during validation or serialization.

---

# 47. AI Agent Mandatory Rules

Before changing Model code, an AI agent MUST:

1. Read this document completely.
2. Treat this document as the authoritative Model standard.
3. Preserve the architectural independence of Model.
4. Identify the domain concept before choosing a Python structure.
5. Use Pydantic v2 only.
6. Use modern Python typing.
7. Prefer explicit domain types over generic containers.
8. Preserve omitted vs null vs generated semantics.
9. Preserve Model rules even when technical representations are partial.
10. Keep persistence concerns out of Model.
11. Keep API transport concerns out of Model.
12. Keep business workflows out of Model.
13. Keep external I/O out of Model.
14. Use `StrEnum` for reusable domain enumerations.
15. Use `Literal` for small local closed sets.
16. Use `Decimal` when exact decimal semantics matter.
17. Preserve timezone semantics explicitly.
18. Use validators only for rules determinable from Model data.
19. Prefer composition over deep inheritance.
20. Reuse one authoritative Model definition.
21. Avoid legacy Pydantic patterns.
22. Verify version-sensitive Pydantic behavior against the installed version or current official documentation when uncertain.
23. Explicitly report a conflict if a requested change would violate this standard.

---

# 48. Decision Order

When multiple implementations are possible, prefer in this order:

1. Domain correctness.
2. Preservation of Model meaning.
3. Clear component boundaries.
4. Type safety.
5. Explicit validation.
6. Current supported Pydantic APIs.
7. Simplicity.
8. Reusability.
9. Maintainability.
10. Additional abstraction only when justified.

---

# 49. At a Glance

## MUST

- Represent meaningful domain entities and concepts.
- Keep one authoritative logical definition per Model.
- Expose the resolved Model set as an independent shared package.
- Provide one documented public import interface.
- Preserve field meaning across all derived technical representations.
- Distinguish omitted, explicit null, supplied, and generated values.
- Preserve partial-update semantics.
- Declare conceptual relationships and cardinality.
- Keep domain rules traceable to Model.
- Validate rules determinable from Model's own data.
- Use modern Pydantic v2.
- Use modern Python typing.
- Use exact domain types where meaning requires them.
- Use deterministic, side-effect-free validation and serialization.
- Include and verify a developer-facing `README.md` for every completed Model package.

## SHOULD

- Prefer `Annotated` + `Field` for reusable field constraints.
- Prefer `StrEnum` for reusable string domain values.
- Prefer `Literal` for small local closed sets.
- Prefer `Decimal` for exact financial values.
- Prefer timezone-aware semantics for real-world instants.
- Prefer composition over inheritance.
- Prefer a stable package-root public import interface.
- Prefer `extra="forbid"` for strict closed domain objects.

## NEVER

- Define a Model because a framework needs a class.
- Treat a database table as the domain definition.
- Treat an API request/response as the domain definition.
- Put SQLAlchemy mappings in Model.
- Put database queries in Model.
- Put FastAPI/HTTP behavior in Model.
- Put business workflows in Model.
- Perform I/O from validation or serialization.
- Replace required values with placeholders.
- Confuse omitted input with explicit null.
- Allow defaults to override explicit Model declarations.
- Duplicate the same logical Model independently in multiple components.
- Introduce Pydantic v1 patterns into new code.

---

# 50. Final Rule

The Model component defines **what the project's domain data means**.

It is the shared logical source used by Database, Backend, Frontend, and other technical components.

Use **Pydantic v2** to implement that shared domain model.

Keep Model independent from persistence, transport, workflows, presentation, and deployment.

Technical layers may derive specialized representations, but they MUST preserve the identity and meaning declared by Model.

When there is a conflict between convenience and these Model Principles, **the Model Principles win**.

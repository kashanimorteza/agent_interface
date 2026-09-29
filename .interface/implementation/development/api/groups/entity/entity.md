# Entity Group Definition

Entity Group is the API Group that publishes the API-enabled capabilities of Logic's Entity Service through one modular external HTTP surface.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Layering](#layering)**
7. **[Authority](#authority)**
8. **[Principles](#principles)**
9. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Entity Group corresponds to Logic's Entity Service. It exposes the Entity Child Services and callable Actions that Entity Service publishes for API generation, while keeping HTTP representation separate from application Behaviour.

There is one Entity Group for the complete Entity Service, not one Group per Entity. Each Entity Child Service becomes a resource inside this Group. The Group's Router owns HTTP representation and its Adapter communicates with Entity Service only through Logic Interface.

### Purpose

External consumers need to work with Model-backed application Entities without importing Logic or knowing how Entity Service reaches Storage and Database. Entity Group translates between HTTP and Entity Service's published contract while preserving the Entity, Action, result, failure, and selected Database Instance meanings already owned below it.

### How It Works

The Group exists when Entity Service has both `publish_in_logic_interface` and `generate_api` enabled. It reads Entity Service Interface through Logic Interface. Every callable Entity Action is included by default unless Entity Service Preferences explicitly disable API generation for that Action.

Router receives and returns HTTP data. Adapter maps validated external input to the matching Entity Child Service Action, calls it through Logic Interface, and returns its declared result or failure for Router to represent. Support exports such as the Database Instance Enum inform the contract but never become Endpoints.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Entity Group Role** — the fixed identity of this Group inside API, independent of its configurable external name.
- **Entity Resource** — the external capability area corresponding to one Entity Child Service published by Entity Service Interface.
- **Router** — the HTTP-facing layer that owns Entity Group routes, requests, responses, transport validation, and public failures.
- **Adapter** — the transport-independent bridge that maps between Router and Entity Service through Logic Interface.
- **Endpoint** — the external HTTP representation of one API-enabled callable Entity Action.
- **Transport Schema** — an external request or response shape owned by Entity Group and derived from a published Action contract; it is not a copied Model Entity.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Entity Group
├── router/
│   └── <entity>
└── adapter/
    └── <entity>
```

The names and patterns shown are defaults selected by Entity Group Preferences. A selected language may realize a small layer compactly or use several files, but the responsibilities and dependency direction remain unchanged.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Belongs to API** — is composed through API Bootstrap as one Group of the shared external boundary.
- **Corresponds to Entity Service** — derives eligibility and Endpoint membership from Entity Service Preferences and its published Interface.
- **Consumes Logic** — invokes Entity Child Service Actions only through Logic Interface.
- **Consumed by external clients** — publishes Entity resources and their API-enabled Actions through HTTP.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Entity meaning and declarations** — belong to Model and reach this Group only through the published Logic contract.
- **Application Behaviour** — belongs to Entity Service and other Logic Services; this Group never reimplements it.
- **Persistence and Database selection mechanics** — remain behind Logic; the Group only carries a valid published Database Instance choice when the Action accepts it.
- **Routes, external shapes, transport validation, serialization, and public failures for Entity capabilities** — belong to Entity Group.
- **API-wide composition, lifecycle, and shared concerns** — belong to root API.
- **Technical HTTP mechanics** — belong to the selected package and implementation skill unless Target or compatible Entity Group Preferences select them.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Entity Group has one dependency direction: Router calls Adapter, and Adapter calls Entity Service through Logic Interface.

### Router

The HTTP-facing boundary. It owns the Group route namespace, Entity resource paths, external requests and responses, transport validation, serialization, and public contract metadata. It calls only Entity Group Adapter and contains no application Behaviour.

### Adapter

The transport-independent bridge to Entity Service. It maps valid external input to the selected Entity Child Service Action, invokes it only through Logic Interface, and returns the declared result or failure toward Router. It contains no HTTP mechanics or persistence implementation.

### Resources and Endpoints

Every Entity Child Service published by Entity Service Interface becomes one Entity Resource. Every callable Action whose API generation is enabled becomes one Endpoint under its owning Resource. Entity Group does not maintain a second Entity or Action catalogue.

### Documentation

Entity Group documentation explains every generated Entity Resource and Endpoint, including accepted input, returned output, declared failures, collection behaviour when supported, and runnable consumer examples.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Entity Group. Entity Group Preferences provide configurable defaults but never weaken a Principle. Explicit Target meaning and applicable API, Logic, and Entity Service Principles retain their authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### Entity Group corresponds to Entity Service only

**Rule:** Entity Group exists only when Entity Service is published through Logic Interface and has API generation enabled. It represents that one Service and no other Logic capability.
**Why:** One source keeps Group ownership and eligibility unambiguous.
**Boundary:** Cross-Service orchestration first becomes a Logic Service capability; Entity Group never coordinates Logic Services itself.

#### Entity Group remains independent of realization

**Rule:** Entity Group fixes responsibilities, dependency direction, and observable capability contracts without requiring a programming language, framework, package, or implementation pattern.
**Why:** Its contract must remain implementable by compatible technology choices.
**Boundary:** Preferences and the selected skill may choose mechanics without changing Entity or Action meaning.

<br>

### Membership

#### Resources follow Entity Child Services

**Rule:** Entity Group creates exactly one Resource for every Entity Child Service published by Entity Service Interface and no Resource for anything else.
**Why:** The external Entity set stays aligned with the authoritative application capability set.
**Boundary:** Entity Group never reads Model directly or invents, copies, or removes an Entity.

#### Endpoints follow callable Action settings

**Rule:** Every callable Action published by an Entity Child Service becomes exactly one Endpoint unless Entity Service Preferences explicitly set `generate_api: false` for that Action. Non-callable exports never become Endpoints.
**Why:** Endpoint membership stays aligned with the authoritative Service contract without a second catalogue.
**Boundary:** Entity Group may change only a compatible external representation; it never creates an Action absent from Entity Service Interface.

#### Entity identities and routes remain unique

**Rule:** The Group identity, resource identities, route prefix, paths, and final method-and-path combinations are valid and unique after the selected realization's declared normalization. A collision or invalid value stops generation with a clear error.
**Why:** Silent renaming changes the public contract and makes routing ambiguous.
**Boundary:** Generation never resolves a conflict with an invented suffix, number, or hidden rename.

<br>

### Router

#### Router owns HTTP representation only

**Rule:** Router owns Entity Group routes, methods, requests, responses, transport validation, serialization, and public failure representation. It calls only Entity Group Adapter and contains no application Behaviour.
**Why:** Keeping HTTP at the edge lets Logic and Adapter remain transport-independent.
**Boundary:** Router never calls Logic, another Group, Database, or Storage Service directly.

#### HTTP mechanics follow the selected realization

**Rule:** Explicit compatible Target or Entity Group Preference choices are preserved. When no such choice exists, the selected package or implementation skill chooses compatible HTTP mechanics and makes the resulting external contract observable.
**Why:** Technical choices should not become permanent conceptual rules or block an otherwise complete Entity capability.
**Boundary:** Realization never changes an Action's meaning, input, result, failure, eligibility, or owning Entity Resource.

#### External schemas follow Entity Action contracts

**Rule:** Each Endpoint derives its request and response from its published Entity Action contract. A distinct Transport Schema may be defined only when the external representation must differ.
**Why:** This preserves Logic authority while allowing a valid HTTP representation.
**Boundary:** Entity Group never copies Domain meaning, changes Model types, or introduces application Behaviour.

#### Collections remain explicit and bounded

**Rule:** Filtering, ordering, and pagination are available only when the matching Entity Action supports them. Public values are allowlisted and bounded and never become direct storage commands.
**Why:** External input must not gain storage capabilities absent from Logic or request an unbounded public result.
**Boundary:** Representation comes from compatible Preferences or the selected package, while capability meaning remains in Entity Service.

#### Public outcomes remain faithful and safe

**Rule:** A successful Endpoint returns its declared Action result without a Group-wide success envelope. Declared failures remain failures, and unexpected failures become a safe public response carrying a non-secret request identifier.
**Why:** Entity Group must preserve capability results without exposing internals or creating another result model.
**Boundary:** HTTP representation never exposes internal exceptions, persistence details, or secrets and never turns a failure into success.

<br>

### Adapter

#### Adapter maps without reimplementing Behaviour

**Rule:** Adapter maps validated external input to the matching Entity Child Service Action, invokes it through Logic Interface, and maps its declared result back toward Router. It contains no HTTP mechanics, application decision, or persistence implementation.
**Why:** A narrow Adapter prevents transport and Behaviour from leaking into one another.
**Boundary:** Adapter may map representation but never changes Entity identity, Database Instance selection, permission, or Action result.

<br>

### Documentation and Verification

#### Entity Group owns a consistent detailed contract

**Rule:** Running routes, machine-readable contract, and human documentation describe the same Entity Resources, Endpoints, requests, responses, and failures.
**Why:** Consumers must not build against a description different from the running Group.
**Boundary:** Root API introduces and combines the Group but never redefines its detailed contract.

#### Verification covers the Entity boundary

**Rule:** Verification confirms eligibility, Resource and Endpoint membership, route uniqueness, Router-to-Adapter-to-Logic dependency direction, contract consistency, bounded collection input, safe failures, and preservation of Entity and Database Instance identities.
**Why:** These are the observable and architectural guarantees consumers rely on.
**Boundary:** Group verification never replaces Entity Service Behaviour or Database persistence verification.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Entity Group corresponds to Entity Service only**

- **Must** — Generate one Entity Group only from eligible Entity Service.
- **Never** — Represent another Service or coordinate Services inside the Group.

**Entity Group remains independent of realization**

- **Must** — Preserve responsibilities, dependency direction, and contracts across compatible realizations.
- **Never** — Make a language, framework, package, or implementation pattern part of this Definition.

### Membership

**Resources follow Entity Child Services**

- **Must** — Create one Resource for each published Entity Child Service.
- **Never** — Read Model directly or maintain another Entity catalogue.

**Endpoints follow callable Action settings**

- **Must** — Create one Endpoint for every API-enabled callable Entity Action.
- **Never** — Publish a support export or Action absent from Entity Service Interface.

**Entity identities and routes remain unique**

- **Must** — Validate every identity and final route combination.
- **Never** — Silently rename an invalid or colliding value.

### Router

**Router owns HTTP representation only**

- **Must** — Keep HTTP representation in Router and call Adapter only.
- **Never** — Put Behaviour in Router or call Logic or persistence directly.

**HTTP mechanics follow the selected realization**

- **Must** — Preserve explicit compatible choices and otherwise document selected mechanics.
- **Never** — Let mechanics change Entity Action meaning.

**External schemas follow Entity Action contracts**

- **Must** — Derive external shapes from published Action contracts.
- **Never** — Invent Domain meaning or application Behaviour.

**Collections remain explicit and bounded**

- **Must** — Expose only supported, allowlisted, and bounded collection input.
- **Never** — Turn public input into a direct storage command or unbounded result.

**Public outcomes remain faithful and safe**

- **Must** — Preserve declared results and failures safely.
- **Never** — Add a universal success envelope or expose private failures.

### Adapter

**Adapter maps without reimplementing Behaviour**

- **Must** — Map to the matching Entity Action through Logic Interface.
- **Never** — Add HTTP mechanics, application decisions, or persistence work.

### Documentation and Verification

**Entity Group owns a consistent detailed contract**

- **Must** — Keep running routes and both contract forms consistent.
- **Never** — Let root API or package mechanics redefine the Group contract.

**Verification covers the Entity boundary**

- **Must** — Verify membership, direction, routes, contract, bounds, failures, and preserved identities.
- **Never** — Replace Logic or Database verification.

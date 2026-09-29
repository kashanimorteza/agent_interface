# Entity Group Definition

Entity Group is the API Group that gives every Entity presented by Entity Service one Adapter containing an Endpoint for every Action of that Entity.

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

Entity Group represents Entity Service as an API Group. Every Entity Child Service published through Logic Interface becomes one Adapter. Every Action presented by that Child Service becomes one Endpoint in the Entity's Adapter.

An Endpoint combines an HTTP Method, a Path, Parameters derived from the Action contract, and a Handler. The Handler receives the request, calls the same Action on the Adapter's bound Entity Child Service, and returns its result unchanged. Entity Group neither performs the Action nor reaches Model, Database, Storage Service, or another system directly.

### Purpose

Entity Service already supplies the authoritative set of Entities and their Actions. Entity Group turns that contract into a consistent HTTP surface without duplicating Entity declarations, Action signatures, or application Behaviour.

### How It Works

Entity Group is created when Entity Service is published through Logic Interface and its Service-level API generation setting is enabled. It creates one Adapter for every Entity Child Service and binds the Adapter to that Child Service's Entity identity.

For every Action presented by a Child Service, the Adapter creates one Endpoint. A known Action uses its configured HTTP Method and Path. An Action without an explicit mapping uses `POST /<action>`. Parameters named by Path placeholders are placed in Path; remaining parameters use Query for `GET` and `DELETE`, and Body for `POST`, `PUT`, and `PATCH`. Parameter names, requirements, structures, meanings, and defaults always come from the Action contract.

The configured Group name forms the Group URL segment, the bound Entity identity forms the Entity segment, and the Action mapping forms the remaining Endpoint Path.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Entity Group** — the API Group generated from Entity Service.
- **Entity** — the identity bound to one Entity Child Service and represented as an API resource.
- **Adapter** — the file for one Entity that contains the Endpoints and Handlers generated from that Entity's Actions.
- **Entity Service Action** — a callable capability presented by an Entity Child Service.
- **Action Mapping** — the configurable HTTP Method and Path for a known Entity Service Action.
- **Endpoint** — the public HTTP Method, Path, Parameters, and Handler generated for one Entity Service Action.
- **Path** — the relative URL pattern of an Endpoint, such as `/update/{id}`.
- **Parameter** — an Action input exposed in Path, Query, or Body according to the Entity Group placement rules.
- **Handler** — the executable part of an Endpoint that receives request values, calls the corresponding Entity Service Action, and returns its result.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Entity Group
├── <entity>  (Adapter)
└── <entity>  (Adapter)
```

Adapter files are placed directly inside the Entity Group directory. There is no intermediate Adapter directory. Every Adapter is bound to one Entity identity presented by Entity Service and contains the Endpoints generated from all Actions of that Entity Child Service.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Belongs to API** — is registered and served as one API Group.
- **Consumes Entity Service through Logic Interface** — obtains every Entity Child Service and its Actions from the published Entity Service boundary and calls those Actions through the same boundary.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Entity membership, Entity identity, Action membership, and Action contracts** — come from Entity Service through Logic Interface; Entity Group does not redefine them.
- **Action Behaviour and work performed after an Action call** — remain behind Entity Service; an Adapter never reaches another Component or system directly.
- **HTTP Method and Path** — come from Entity Group Action Mappings or the declared fallback.
- **Parameter names, requirements, structures, meanings, and defaults** — come from the Entity Service Action contract; Entity Group only determines their HTTP placement.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Entity Group has one executable layer: Adapters. Each Adapter owns the API surface of one Entity and its Handlers call only Actions of that Entity Child Service through Logic Interface.

### Adapters

The Entity Group directory contains exactly one Adapter file for every Entity Child Service presented by Entity Service. The Adapter filename and Entity URL segment derive from the bound Entity identity, not from a language-specific Child Service structure name. Selecting an Adapter selects its Entity once; callers do not supply an Entity class or Entity name again.

Every Adapter contains one Endpoint and Handler for every Action presented by its bound Child Service. An Adapter neither removes a presented Action nor adds an Action that Entity Service does not present.

### Endpoints

Each Endpoint uses the Action Mapping for its Entity Service Action. When no explicit mapping exists, the Endpoint uses `POST /<action>`. Path placeholders select Path Parameters. Remaining Action inputs become Query Parameters for `GET` and `DELETE`, or Body Parameters for `POST`, `PUT`, and `PATCH`.

The Handler performs only the structural request binding needed by the Endpoint, calls the corresponding Action on the bound Entity Child Service, and returns the Action result unchanged. Semantic validation, application decisions, persistence, retries, and result transformation remain outside Entity Group.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Entity Group. Entity Group Preferences provide configurable names and Action Mapping defaults but cannot weaken a Principle. Explicit compatible project meaning and applicable API and Entity Service Principles retain their authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### Entity Group represents Entity Service only

**Rule:** Entity Group obtains Entities and Actions only from Entity Service through Logic Interface and calls those Actions only through the same boundary. It represents no other Service or capability.
**Why:** One source keeps every Adapter and Endpoint aligned with the authoritative Entity-facing contract.
**Boundary:** Entity Group publishes Endpoints but neither performs Entity Service work nor contacts Model, Database, Storage Service, or another system directly.

#### Entity Group generation is controlled at Service level

**Rule:** Entity Group is created only when Entity Service is published through Logic Interface and its Service-level API generation setting is enabled. Once created, the Group includes every Entity and every Action that Entity Service presents.
**Why:** One decision controls publication of the complete Entity contract without producing a partial and misleading API surface.
**Boundary:** Entity Group applies no per-Entity or per-Action API-generation filter.

<br>

### Adapters

#### Every Entity receives one Adapter

**Rule:** Entity Group creates exactly one Adapter file for every Entity Child Service presented by Entity Service and no Adapter for anything else. The Adapter is permanently bound to that Child Service's Entity identity.
**Why:** Each Entity needs one predictable API surface without requiring callers to repeat its identity in every request.
**Boundary:** An Adapter never changes its bound Entity and never accepts another Entity identity from a caller.

#### Every Action receives one Endpoint

**Rule:** Every Adapter contains exactly one Endpoint for every Action presented by its bound Entity Child Service. An Action outside the Child Service is never added, and a presented Action is never omitted.
**Why:** The API surface remains a complete representation of the authoritative Entity Service contract.
**Boundary:** Entity Group defines HTTP exposure only; it does not copy, redefine, or implement an Action.

#### Handlers only call corresponding Entity Service Actions

**Rule:** A Handler binds the request values required by its Action, calls that Action on the Adapter's bound Entity Child Service, and returns the result unchanged.
**Why:** Entity Service remains the single owner of Behaviour while Adapter code stays uniform and direct.
**Boundary:** A Handler adds no application decision, semantic validation, persistence operation, result wrapper, downstream call, retry, or alternate execution path.

<br>

### Endpoints

#### Action Mappings define known HTTP identities

**Rule:** Entity Group Preferences may provide an HTTP Method and Path for a known Entity Service Action. An Action without an explicit mapping uses `POST /<action>`. A compatible Target choice may override a default Method or Path without changing the destination Action or its Behaviour.
**Why:** Known Actions receive intentional public identities while every future Action remains exposable without inventing application Behaviour.
**Boundary:** An Action Mapping defines only HTTP Method and Path; the Action contract remains authoritative for every input and result.

#### Endpoint Parameters preserve Action contracts

**Rule:** Every Endpoint derives its Parameters from the corresponding Entity Service Action contract. Parameters named by Path placeholders use Path; remaining parameters use Query for `GET` and `DELETE`, and Body for `POST`, `PUT`, and `PATCH`.
**Why:** Endpoint generation must not duplicate or drift from Action signatures while still placing inputs predictably in HTTP requests.
**Boundary:** Entity Group performs structural request binding only and never changes a Parameter's name, requirement, structure, meaning, default, or semantic validation owner.

#### Adapter identities and Endpoints are unique

**Rule:** Every Adapter filename, Entity URL segment, and final Method-and-Path combination is valid and unique after the selected realization's declared normalization. A collision or invalid value stops creation with a clear error.
**Why:** Two Entities or Actions cannot share one ambiguous public identity.
**Boundary:** Entity Group never repairs a conflict with an invented suffix, number, or silent rename.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Entity Group represents Entity Service only**

- **Must** — Obtain Entities and Actions from Entity Service through Logic Interface and call Actions through the same boundary.
- **Never** — Represent another capability or contact another Component or system directly.

**Entity Group generation is controlled at Service level**

- **Must** — Generate the Group only when Entity Service publication and API generation are enabled, then include its complete presented contract.
- **Never** — Filter an individual Entity or Action from an enabled Entity Group.

### Adapters

**Every Entity receives one Adapter**

- **Must** — Create exactly one Adapter bound to every Entity Child Service.
- **Never** — Accept another Entity identity or create an Adapter for anything Entity Service does not present.

**Every Action receives one Endpoint**

- **Must** — Generate one Endpoint for every Action of the Adapter's bound Entity Child Service.
- **Never** — Add an unknown Action or omit a presented Action.

**Handlers only call corresponding Entity Service Actions**

- **Must** — Bind request values, call the corresponding Action, and return its result unchanged.
- **Never** — Add Behaviour, semantic validation, persistence, a result wrapper, a downstream call, a retry, or an alternate path.

### Endpoints

**Action Mappings define known HTTP identities**

- **Must** — Use the configured Method and Path or the `POST /<action>` fallback without changing the destination Action.
- **Never** — Put Action inputs, results, or Behaviour into an Action Mapping.

**Endpoint Parameters preserve Action contracts**

- **Must** — Derive every Parameter from the Action contract and place it according to Method and Path.
- **Never** — Redefine a Parameter or invent a Group-level default.

**Adapter identities and Endpoints are unique**

- **Must** — Validate Adapter identities, Entity URL segments, and final Method-and-Path combinations.
- **Never** — Silently rename an invalid or colliding value.

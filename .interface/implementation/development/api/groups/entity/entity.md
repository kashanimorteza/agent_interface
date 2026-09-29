# Entity Group Definition

Entity Group is the API Group that gives every Entity Resource one Adapter containing the fixed Entity Endpoints.

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

Entity Group is the API capability area for Entity Service. Every Entity presented by Entity Service becomes one Resource with one Adapter. Each Adapter contains one Endpoint for every fixed Entity Operation.

An Endpoint combines an HTTP Method, a Path, and its Parameters. Its Handler receives a request, calls the corresponding Logic Action for the Adapter's bound Resource, and returns the Logic Action result. Entity Group does not perform the requested operation itself and does not call a system behind Entity Service directly.

### Purpose

Every Entity Resource exposes the same Operation set, but each one needs its own URL segment and bound identity. Entity Group creates that repeated API surface from one fixed Endpoint catalogue and one Adapter per Resource.

Without this Group, each Resource Endpoint would have to be declared separately, the same Operation mapping could drift between Resources, and callers could not rely on one predictable address structure.

### How It Works

Entity Group is available when Entity Service is published through Logic Interface and API generation is enabled for the Service. It reads the Entities presented by Entity Service and treats each one as an API Resource with one bound Adapter.

Every Adapter receives the fixed Endpoints for Add, Update, List, Delete, Enable, Disable, Get by ID, Count, Sum, Min, Max, and Truncate. An Endpoint Handler receives its declared Path, Query, and Body Parameters, supplies its bound Resource where the Logic Action requires it, calls the corresponding Logic Action through Entity Service in Logic Interface, and returns that result.

The Group name forms the Group URL segment. The Resource name forms the Resource segment. The final Path and HTTP Method come from the fixed Endpoint entry in Entity Group Preferences.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Entity Group** — the API Group containing the Adapters generated for Entity Resources.
- **Resource** — one Entity presented through Entity Service and bound to exactly one Adapter.
- **Adapter** — the file for one Resource that declares and handles that Resource's fixed Endpoints.
- **Entity Operation** — one member of the fixed Add, Update, List, Delete, Enable, Disable, Get by ID, Count, Sum, Min, Max, and Truncate catalogue.
- **Endpoint** — one public combination of HTTP Method, Path, Parameters, and Handler representing an Entity Operation.
- **Path** — the relative URL pattern of an Endpoint, such as `/update/{id}`.
- **Parameter** — one declared Path, Query, or Body input accepted by an Endpoint.
- **Handler** — the function inside an Adapter that receives Endpoint Parameters, calls the corresponding Logic Action, and returns its result.
- **Logic Action** — the Entity Service capability invoked by an Endpoint Handler.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Entity Group
└── adapters/
    └── <resource>
        └── <endpoint handlers>
```

The Adapters directory and Adapter filename pattern are defaults selected by Entity Group Preferences. Every generated Adapter is bound to one Entity Resource and contains the complete fixed Entity Endpoint set.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Belongs to API** — is registered and served beneath the Entity Group name by the shared API boundary.
- **Consumes Entity Service through Logic Interface** — discovers Entity Resources and calls their Logic Actions through the published Entity Service boundary.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **The shared API process, Base URL, optional URL Key, and Group registration** — belong to root API.
- **Resource membership and Logic Action contracts** — come from Entity Service through Logic Interface; Entity Group does not redefine them.
- **Work performed after a Logic Action is called** — remains behind Entity Service; an Adapter never reaches another system directly.
- **HTTP Method, Path, and placement of external Parameters** — belong to Entity Group and are declared in Entity Group Preferences.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Entity Group has one executable layer: Adapters. Each Adapter owns the API surface of one Entity Resource and its Handlers call only the corresponding Logic Actions through Logic Interface.

### Adapters

The configured Adapters directory contains exactly one Adapter file for every Entity Resource presented by Entity Service. Selecting an Adapter selects its bound Resource once; callers do not supply an Entity class or Entity name again.

Every Adapter contains the same twelve Endpoints and their Handlers. Each Handler receives only its Endpoint's declared Parameters, adds the bound Resource where required by the Logic Action, calls that Action, and returns its result unchanged.

### Endpoints

Add receives a Resource representation in the Body. Update receives a record ID in the Path and a complete Resource representation in the Body. List receives its optional collection Parameters through Query. Delete, Enable, Disable, and Get by ID receive a record ID through Path. Count receives optional filtering Parameters through Query. Sum, Min, and Max additionally receive a Field through Query. Truncate receives no Resource representation or record ID.

Every Endpoint may receive the optional Instance Parameter published by Entity Service and passes it unchanged. When Instance is omitted, Entity Group makes no selection of its own.

### Documentation

Entity Group owns documentation for its Group address, generated Resource Adapters, fixed Endpoints, Methods, Paths, Parameters, and examples. The documentation is derived from the generated Adapter set and Endpoint catalogue in Entity Group Preferences. Whether Group documentation is presented within one combined API document or separately is a composition choice outside this Group's capability contract.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Entity Group. Entity Group Preferences provide configurable defaults and the fixed Endpoint catalogue but cannot weaken a Principle. Explicit compatible project meaning and applicable API and Entity Service Principles retain their authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### Entity Group represents Entity Service only

**Rule:** Entity Group discovers Resources and calls Logic Actions only through Entity Service in Logic Interface. It represents no other service or capability.
**Why:** One source keeps every Adapter and Endpoint bound to the same authoritative Entity capability set.
**Boundary:** Entity Group publishes Endpoints but neither performs Entity Service work nor contacts a system behind that Service directly.

<br>

### Adapters

#### Every Entity Resource receives one Adapter

**Rule:** Entity Group creates exactly one Adapter file for every Entity Resource presented by Entity Service and no Adapter for anything else. The Adapter is bound to that Resource for every Endpoint it contains.
**Why:** Each Resource needs one predictable API address without requiring callers to repeat or select its identity inside every request.
**Boundary:** An Adapter never changes its bound Resource and never accepts another Entity identity from a caller.

#### Every Adapter contains the fixed Entity Endpoint set

**Rule:** Every Adapter contains exactly one Endpoint for Add, Update, List, Delete, Enable, Disable, Get by ID, Count, Sum, Min, Max, and Truncate. The set is fixed by Entity Group and is not filtered through per-Action API-generation overrides.
**Why:** Every Entity Resource needs the same complete and predictable API surface.
**Boundary:** Any capability outside this fixed Entity Operation set does not become an Entity Endpoint.

#### Handlers only call corresponding Logic Actions

**Rule:** An Endpoint Handler receives its declared Parameters, supplies its Adapter's bound Resource where required, calls the corresponding Logic Action through Logic Interface, and returns the result unchanged.
**Why:** Entity Service remains the single owner of the work while Adapter code stays uniform and direct.
**Boundary:** A Handler adds no application decision, result wrapper, downstream call, retry, or alternate execution path.

<br>

### Endpoints

#### Every Entity Operation has one explicit Endpoint

**Rule:** Entity Group Preferences declare exactly one HTTP Method, Path, Parameter contract, and Logic Action for every fixed Entity Operation. Every Adapter uses that same Endpoint mapping.
**Why:** Explicit mappings make the public API predictable and prevent different Adapters from representing the same Operation differently.
**Boundary:** Root API supplies the Base URL and Group segment; Entity Group supplies the Resource and Endpoint segments.

#### Endpoint Parameters preserve Logic Action inputs

**Rule:** Every Endpoint exposes the Path, Query, and Body Parameters required to call its corresponding Logic Action. Optional values remain optional, and an omitted value is not replaced by an Entity Group default.
**Why:** Handlers must carry requests without changing the Logic Action contract or inventing query behaviour.
**Boundary:** Entity Group chooses external Parameter placement but never changes Parameter meaning, validation ownership, or downstream defaults.

#### Adapter identities and Endpoints are unique

**Rule:** Every Adapter filename, Resource segment, and final Method-and-Path combination is valid and unique after the selected realization's declared normalization. A collision or invalid value stops creation with a clear error.
**Why:** Two Resources or Entity Operations cannot share one ambiguous public address.
**Boundary:** Entity Group never repairs a conflict with an invented suffix, number, or silent rename.

<br>

### Documentation

#### Entity Group documents its generated API surface

**Rule:** Entity Group documentation presents the Group address, every generated Resource Adapter, every fixed Endpoint, its Method, Path, Parameters, Logic Action, and usable examples from the same definitions used to create the running Group.
**Why:** Callers need documentation that matches the Entity Endpoints they can actually invoke.
**Boundary:** Documentation does not copy private implementation or define a Resource, Logic Action, or result absent from Entity Service.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Entity Group represents Entity Service only**

- **Must** — Discover Resources and call Logic Actions only through Entity Service in Logic Interface.
- **Never** — Represent another capability or contact a system behind Entity Service directly.

### Adapters

**Every Entity Resource receives one Adapter**

- **Must** — Create exactly one bound Adapter for every Entity Resource.
- **Never** — Accept another Entity identity or create an Adapter for a non-Entity Resource.

**Every Adapter contains the fixed Entity Endpoint set**

- **Must** — Include exactly the twelve fixed Entity Endpoints in every Adapter.
- **Never** — Include a capability outside the fixed Entity Operation set or filter Endpoints through per-Action API-generation settings.

**Handlers only call corresponding Logic Actions**

- **Must** — Forward declared Parameters to the corresponding Logic Action and return its result unchanged.
- **Never** — Add Behaviour, a result wrapper, a downstream call, a retry, or an alternate path.

### Endpoints

**Every Entity Operation has one explicit Endpoint**

- **Must** — Use the configured Method, Path, Parameters, and Logic Action consistently in every Adapter.
- **Never** — Let Adapters invent different Endpoint mappings for the same Entity Operation.

**Endpoint Parameters preserve Logic Action inputs**

- **Must** — Expose and forward every required and optional Logic Action input without adding Group defaults.
- **Never** — Change Parameter meaning or replace an omitted value.

**Adapter identities and Endpoints are unique**

- **Must** — Validate Adapter identities, Resource segments, and final Method-and-Path combinations.
- **Never** — Silently rename an invalid or colliding value.

### Documentation

**Entity Group documents its generated API surface**

- **Must** — Document generated Adapters and Endpoints from their actual definitions.
- **Never** — Document a Resource, Logic Action, result, or private implementation absent from Entity Service.

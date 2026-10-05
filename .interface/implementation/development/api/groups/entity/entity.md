# Entity Group Definition

Entity Group is the API Group that gives every Entity of Entity Service one Adapter holding an Endpoint for every Action of that Entity.

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

Entity Group is the API Group that turns Entity Service into HTTP: one Adapter for every Entity, and one Endpoint for every Action of that Entity.

### Purpose

Entity Service already holds every Entity and its Actions. Entity Group gives them one consistent HTTP surface without repeating their contracts or adding Behaviour.

### How It Works

A request reaches an Endpoint; its Handler calls the same Action on the Entity's Child Service through Logic Interface and returns the result unchanged.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Adapter** — the unit for one Entity that holds the Endpoints of that Entity's Actions.
- **Action** — one operation an Entity Child Service offers.
- **Handler** — the part of an Endpoint that binds the request, calls its Action, and returns the result.
- **API Group Interface Schema** — the versioned contract through which every Group states what it serves.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Entity Group
├── <entity>   ← Adapter: the Endpoints of one Entity
└── <entity>   ← Adapter
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Logic** — uses Entity Service and the contracts it publishes only through Logic Interface, found from Logic's own Preferences.
- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Entity and Action membership and Action contracts** — are not Entity Group's, because it represents them without defining them.
- **Action Behaviour and everything after an Action call** — are not Entity Group's, because a Handler only calls the Action.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Entity Group Preferences own its name, directory, Adapter naming pattern, and documentation. The shape in which it states them belongs to the API Group Interface Schema.

### Adapters

One unit for every Entity Child Service, placed directly inside the Entity Group directory and named from the bound Entity. Selecting an Adapter selects its Entity once; a caller never supplies the Entity again.

### Endpoints

The HTTP surface of every Adapter. It meets these needs:

1. **Complete** — exactly one Adapter for every Entity that Entity Service presents, and exactly one Endpoint for every Action of that Entity, changing when Entity Service changes.
2. **Unchanged** — every Parameter keeps the Action's name, requirement, structure, and default, and every Endpoint returns the Action's result and errors unchanged.
3. **Nothing else** — no Endpoint or Behaviour beyond these is added.

These needs are stated in the shape the API Group Interface Schema defines for every Group.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Entity Group. Entity Group Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning retains its authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### Entity Group reaches the application only through Logic Interface

**Rule:** Entity Group obtains Entities, Actions, and their public contracts only from Entity Service through Logic Interface, and calls Actions only through that same boundary.
**Why:** One source keeps every Adapter and Endpoint aligned with the authoritative contract.
**Boundary:** Entity Group publishes Endpoints but never performs an Action's work.

### Interface

#### Entity Group conforms to the API Group Interface Schema

**Rule:** Entity Group states what it serves through the versioned API Group Interface Schema: Entity Service through Logic Interface as its source, one Adapter per Entity, and one Endpoint per Action.
**Why:** Every client depends on one exact HTTP surface instead of reinterpreting each realization.
**Boundary:** Changing the structure itself requires a Schema version change.

### Adapters

#### One Adapter per Entity, one Endpoint per Action

**Rule:** Entity Group has exactly one Adapter for every Entity Child Service that Entity Service presents, permanently bound to that Entity, and each Adapter has exactly one Endpoint for every Action of its Child Service.
**Why:** The HTTP surface stays a complete representation of Entity Service, and callers never repeat an Entity's identity.
**Boundary:** No Entity or Action is filtered out, no Action outside the Child Service is added, and an Adapter never accepts another Entity from a caller.

#### Handlers only call their Action

**Rule:** A Handler binds the request values its Action needs, obtains the bound Child Service through Logic Interface, calls that Action, and returns the result unchanged.
**Why:** Entity Service stays the single owner of Behaviour while every Handler stays uniform.
**Boundary:** A Handler adds no decision, semantic validation, initialization, result wrapper, other call, retry, or alternate path.

### Review

#### Entity Group conformance covers every Entity Group contract

**Rule:** Entity Group is conformant only when its Endpoint needs in this Definition and its real Endpoints match, its statement follows the API Group Interface Schema, and every observation below holds.
**Why:** A gap here silently hides or breaks an Action for every client.
**Boundary:** Review reads Logic Interface only to compare; it changes nothing outside Entity Group.

#### Review observes Entity Group through a fixed set of checks

**Rule:** Review establishes Entity Group conformance through these observations, every one of them on every review:
- Entity Group states its source, Adapters, and Endpoints in the shape the API Group Interface Schema defines.
- There is exactly one Adapter for every Entity that Entity Service presents, and nothing else.
- Every Adapter has exactly one Endpoint for every Action of its Child Service, and nothing else.
- Every Endpoint's Parameters keep the Action's names, requirements, and defaults.
- Every Handler calls only its Action through Logic Interface and returns its result and errors unchanged.
- Entity Group imports nothing but Logic Interface for the application.
**Why:** A fixed set of observations proves the same things on every review, so a result is never judged by a different standard from one run to the next.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it; how it is realized belongs to the Review Operation.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Entity Group reaches the application only through Logic Interface**

- **Must** — Obtain Entities, Actions, and contracts from Entity Service through Logic Interface and call Actions the same way.
- **Never** — Perform an Action's work inside Entity Group.

### Interface

**Entity Group conforms to the API Group Interface Schema**

- **Must** — Conform every realization to the API Group Interface Schema.
- **Never** — Add anything the Schema does not list or change its structure without a Schema version change.

### Adapters

**One Adapter per Entity, one Endpoint per Action**

- **Must** — Give every Entity one bound Adapter and every Action one Endpoint.
- **Never** — Filter an Entity or Action, add an unknown Action, or accept another Entity from a caller.

**Handlers only call their Action**

- **Must** — Bind request values, call the bound Child Service's Action through Logic Interface, and return the result unchanged.
- **Never** — Add a decision, validation, initialization, wrapper, other call, retry, or alternate path.

### Review

**Entity Group conformance covers every Entity Group contract**

- **Must** — show that the Endpoint needs and the real Endpoints match and follow the API Group Interface Schema before Entity Group is conformant.
- **Never** — change anything outside Entity Group during review.

**Review observes Entity Group through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.

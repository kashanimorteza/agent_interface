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
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Entity Group is the API Group that turns Entity Service into API Endpoints: one Adapter for every Entity, and one Endpoint for every Action of that Entity.

### Purpose

Entity Service already holds every Entity and its Actions. Entity Group gives them one consistent API surface without repeating their contracts or adding Behavior.

### How It Works

A request reaches an Endpoint; its Handler calls the same Action on the Entity's Child Service through Logic Interface and returns the result unchanged.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Adapter** — the unit for one Entity that holds the Endpoints of that Entity's Actions.
- **Action** — one operation an Entity Child Service offers.
- **Handler** — the part of an Endpoint that calls its Action and returns the result.
- **Group contract** — the versioned contract, stated in the API Definition, through which every Group states what it serves.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Entity Group
├── Adapters
├── Endpoints
└── Documentation
```

Every entity below is declared in `architecture` in Entity Group Preferences, which also own its name, Adapter naming pattern, and documentation choices. Entity Group states what it serves in the shape of the Group contract in the API Definition: its source is Entity Service, reached through Logic Interface, whose Service group gives the Child Services and whose Model and Database groups give the types its Parameters use.

<!-------------------------- Adapters -->
### Adapters

```text
Adapters
└── one Adapter per Entity
```

One unit for every Entity Child Service, placed directly inside the Entity Group directory and named from the bound Entity. Selecting an Adapter selects its Entity once; a caller never supplies the Entity again.

<!-------------------------- Endpoints -->
### Endpoints

The API surface of every Adapter. It meets these needs:

1. **Complete** — exactly one Adapter for every Entity that Entity Service presents, and exactly one Endpoint for every Action of that Entity, changing when Entity Service changes.
2. **Unchanged** — every Parameter keeps the Action's name, requirement, structure, and default, and every Endpoint returns the Action's result and errors unchanged.
3. **Nothing else** — no Endpoint or Behavior beyond these is added.

<!-------------------------- Documentation -->
### Documentation

```text
Documentation
├── Overview
├── Endpoints
├── Use
└── Verify
```

The documentation of Entity Group, in the file, location, and format Entity Group Preferences name. Its sections, in this order:

1. **Overview** — What Entity Group is, in one paragraph, with one request example.
2. **Endpoints** — Every Entity's Endpoints with Method, Path, and Parameters, each with one example.
3. **Use** — How a client calls an Endpoint.
4. **Verify** — How to see that every Entity and Action has its Endpoint.

<!-------------------------- Directory Structure -->
### Directory Structure

```text
Directory Structure
├── <adapter>
└── README
```

The root of this tree is the Entity Group directory, named in `settings` in Entity Group Preferences. It holds one unit per Adapter, named by the Adapter pattern.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Logic** — uses Entity Service and the contracts it publishes only through Logic Interface, found from Logic's own Preferences.
- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Entity and Action membership and Action contracts** — are not Entity Group's, because it represents them without defining them.
- **Action Behavior and everything after an Action call** — are not Entity Group's, because a Handler only calls the Action.

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

#### Entity Group conforms to the Group contract

**Rule:** Entity Group states its source, Adapters, and Endpoints in the shape the versioned Group contract defines.
**Why:** Every client depends on one exact API surface instead of reinterpreting each realization.
**Boundary:** Changing the structure itself requires raising the Group contract version in API Preferences.

<br>

### Adapters

#### One Adapter per Entity, one Endpoint per Action

**Rule:** Entity Group has exactly one Adapter for every Entity Child Service that Entity Service presents, permanently bound to that Entity, and each Adapter has exactly one Endpoint for every Action of its Child Service.
**Why:** The API surface stays a complete representation of Entity Service, and callers never repeat an Entity's identity.
**Boundary:** No Entity or Action is filtered out, no Action outside the Child Service is added, and an Adapter never accepts another Entity from a caller.

<br>

### Endpoints

#### Handlers only call their Action

**Rule:** A Handler calls only its Action on the bound Child Service and returns its result and errors unchanged.
**Why:** Entity Service stays the single owner of Behavior while every Handler stays uniform.
**Boundary:** A Handler follows the Handler rule of the Group contract in the API Definition.

<br>

### Review

#### Entity Group conformance covers every Entity Group contract

**Rule:** Entity Group is conformant only when its Endpoint needs in this Definition and its real Endpoints match, its statement follows the Group contract, and every observation below holds.
**Why:** A gap here silently hides or breaks an Action for every client.
**Boundary:** Review reads Logic Interface only to compare; it changes nothing outside Entity Group.

#### Review observes Entity Group through a fixed set of checks

**Rule:** Review establishes Entity Group conformance through these observations, every one of them on every review:
- Entity Group states its source, Adapters, and Endpoints in the shape the Group contract defines.
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

**Entity Group conforms to the Group contract**

- **Must** — Conform every realization to the Group contract.
- **Never** — Add anything the contract does not list or change its structure without raising its version.

<br>

### Adapters

**One Adapter per Entity, one Endpoint per Action**

- **Must** — Give every Entity one bound Adapter and every Action one Endpoint.
- **Never** — Filter an Entity or Action, add an unknown Action, or accept another Entity from a caller.

<br>

### Endpoints

**Handlers only call their Action**

- **Must** — Call only the bound Child Service's Action and return the result unchanged.
- **Never** — Add a decision, validation, initialization, wrapper, other call, retry, or alternate path.

<br>

### Review

**Entity Group conformance covers every Entity Group contract**

- **Must** — show that the Endpoint needs and the real Endpoints match and follow the Group contract before Entity Group is conformant.
- **Never** — change anything outside Entity Group during review.

**Review observes Entity Group through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.

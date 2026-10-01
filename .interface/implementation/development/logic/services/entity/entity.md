# Entity Service Definition

Entity Service is the fixed internal Logic Service whose Interface gives every Entity published by Model one Child Service that works through Storage Service.

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

Entity Service is a fixed internal Service of every Logic Component. For every Entity in Model's Entity Collection it provides one Child Service, so a caller selects an Entity once and then calls its Actions without passing the Entity again. Its Interface publishes these Child Services and republishes every contract Storage Interface publishes, except the Storage gateway.

### Purpose

Storage Service takes the Entity on every request. Entity Service binds that Entity once per Child Service and gives each Entity one place for Behaviour of its own.

### How It Works

A caller selects a Child Service and calls an Action; the Child Service adds its bound Entity to the request and hands it to Storage, then returns Storage's answer unchanged.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Entity Role** — the fixed identity of this Service inside Logic, independent of its configurable name.
- **Base** — the one shared structure that holds every Action and that every Child Service receives.
- **Child Service** — the structure bound to one Entity of Model's Entity Collection.
- **Action** — one operation of Base, named and shaped exactly like one Storage Action that takes an Entity, without the Entity class.
- **Logic Entity Interface Schema** — the versioned structure that fixes the exact shape of Entity Service Interface.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Entity Service
├── Interface   ← the Child Services and contracts, in the shape the Logic Entity Interface Schema defines
├── Base        ← the shared structure that offers every Action
└── Entities    ← one Child Service per Entity
```

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Model** — uses the Entity Collection Model Interface publishes to know which Child Services exist, and each Entity it publishes by name to bind one, found from Model's own Preferences.
- **Consumes Storage** — uses every Storage Action that takes an Entity and every contract Storage Interface publishes, only through Storage Interface, found from Storage's own Preferences.
- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Entity meaning and declarations** — are not Entity Service's, because it binds Entities without defining them.
- **Persistence and Instance selection** — are not Entity Service's, because it only requests Storage Actions.
- **Actions that take no Entity** — are not Entity Service's, because a Child Service is bound to one Entity.
- **Publishing Services from Logic's root** — is not Entity Service's, because it owns only its own Interface.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Entity Service Preferences own its configurable name, directory, layout, naming patterns, language and realization, and documentation. The shape of its Interface belongs to the Logic Entity Interface Schema.

### Interface

The gateway callers import from. It publishes the Child Services and every contract Storage Interface publishes, except the Storage gateway. It meets these needs:

1. **Complete** — exactly one Child Service for every Entity in Model's Entity Collection, changing when the Collection changes.
2. **Needed contracts** — every contract Storage Interface publishes, except the Storage gateway, is republished as the original object, never a copy, so no caller has to reach Storage or Database directly.
3. **Nothing else** — Base, the Storage gateway, and anything beyond these are never published, and loading the Interface has no side effect.

The exact shape of these needs is fixed by the Logic Entity Interface Schema, which is built from them. These needs are the reference: when the two differ, the Schema is corrected to match them.

### Base

The layer that holds the one shared structure, in one unit, and every Action. When it is created, it takes one access to Storage, and every Action uses that same access. For every Storage Action that takes an Entity, in the order Storage publishes them, it offers one Action with the same name and the same parameters, except that a parameter taking the Entity class is removed and supplied from the bound Entity; a parameter taking an Entity instance stays. The Action hands the request to Storage and returns its answer and errors unchanged, with one exception: an instance that is not of the bound Entity is rejected with the Invalid Input error Storage Interface republishes, before Storage is called.

### Entities

The layer that holds one unit and one Child Service for every Entity in Model's Entity Collection. Each Child Service receives Base, binds its own Entity, and holds only Behaviour or Actions specific to that Entity.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Entity Service. Entity Service Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning and applicable Logic Principles retain their authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### Entity Service is fixed and internal

**Rule:** Every Logic contains the fixed Entity Role and its Interface. Its configured name may change, but its Role and responsibilities do not. Its implementation remains internal in every case.
**Why:** Entity-oriented access needs one stable gateway without exposing shared or child implementation.
**Boundary:** Base and Storage internals are never exposed.

### Interface

#### Entity Service Interface conforms to the Logic Entity Interface Schema

**Rule:** Every realization of Entity Service Interface conforms to the versioned Logic Entity Interface Schema, which fixes its Child Services, their Actions, the republished contracts, and what it never publishes.
**Why:** Every caller depends on one exact gateway instead of reinterpreting each realization.
**Boundary:** Changing the structure itself requires a Schema version change.

#### Entity Service names are valid and unique

**Rule:** The configured Service name, the Base name, and every Child Service unit and structure name derived from the configured patterns are valid for the selected language and never collide with each other or with a republished contract.
**Why:** Every Entity needs an unambiguous realization that the selected language accepts.
**Boundary:** An invalid, reserved, or colliding value stops generation with a clear configuration error. The generator never invents a suffix, number, or silent rename.

### Base

#### Base mirrors every Storage Action that takes an Entity

**Rule:** Base has exactly one Action for every Storage Action that takes an Entity, in Storage's order, with the same name and parameters except the removed Entity class. No Action is named or listed by hand.
**Why:** Base follows Storage one to one, so whoever knows Storage already knows every Child Service.
**Boundary:** A Storage Action that takes no Entity never becomes an Action.

#### Every Action works only through Storage Interface

**Rule:** Every Action calls its Storage Action through Storage Interface, using the one Storage access Base took when it was created, and returns its answer and errors unchanged.
**Why:** One route keeps every Action a faithful mirror of Storage and keeps persistence out of Entity Service.
**Boundary:** An Action never reaches Database or a Storage implementation detail.

#### Every Action keeps to its bound Entity

**Rule:** An Action that takes an Entity instance rejects an instance that is not of the bound Entity with the Invalid Input error Storage Interface republishes, before calling Storage.
**Why:** Selecting a Child Service must reliably select the Entity the Action works on.
**Boundary:** This checks Entity identity only; it never checks Field values.

### Entities

#### Every Entity has exactly one Child Service

**Rule:** Entity Service has exactly one Child Service for every Entity in Model's Entity Collection. Each binds its own Entity and receives Base.
**Why:** The Child Services stay complete and in step with Model.
**Boundary:** A Child Service never copies or redefines its Entity.

#### A Child Service holds only what is its own

**Rule:** A Child Service holds only Behaviour or Actions specific to its Entity; everything shared comes from Base.
**Why:** Shared Actions are written once and cannot drift between Entities.
**Boundary:** A Child Service may override a Base Action for its own Entity but never detaches itself from Base.

### Review

#### Entity conformance covers every Entity contract

**Rule:** Entity Service is conformant only when its Interface needs in this Definition, the Logic Entity Interface Schema, and its real Interface all match one another.
**Why:** A gap or a change here silently breaks every caller of Entity Service.
**Boundary:** Review reads Model and Storage Interfaces only to compare; it changes nothing outside Entity Service.

#### Review observes Entity Service through a fixed set of checks

**Rule:** Review establishes Entity conformance through these observations, every one of them on every review:
- Every need of the Interface, Base, and Entities layers in this Definition appears in the Logic Entity Interface Schema, and the Schema holds nothing beyond them.
- Entity Service Interface publishes exactly one Child Service for every Entity in Model's Entity Collection, and every contract Storage Interface publishes except the Storage gateway, and nothing else.
- Every republished contract is the identical object Storage Interface publishes.
- Base has exactly one Action for every Storage Action that takes an Entity, in Storage's order, with the same name.
- Each Action has Storage's parameter names, order, and defaults, without the Entity class parameter.
- Each Action returns its Storage Action's result and raises its errors unchanged, and rejects an instance of another Entity with the Invalid Input error.
- Every Action uses the one Storage access Base holds.
- Every Child Service unit and structure name follows the configured patterns, and every name is valid and unique.
- Every Child Service binds exactly its own Entity and receives Base.
- Loading the Interface opens no connection and creates no data or file.
**Why:** A fixed set of observations proves the same things on every review, so a result is never judged by a different standard from one run to the next.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it; how it is realized belongs to the Review Operation.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Entity Service is fixed and internal**

- **Must** — Include the Entity Role and its Interface in every Logic.
- **Never** — Expose Base, Child implementation, or Storage internals.

### Interface

**Entity Service Interface conforms to the Logic Entity Interface Schema**

- **Must** — Conform every realization to the Logic Entity Interface Schema.
- **Never** — Publish anything the Schema does not list or change its structure without a Schema version change.

**Entity Service names are valid and unique**

- **Must** — Keep the Service name, the Base name, and every derived Child name valid and free of collision.
- **Never** — Resolve a collision by inventing a suffix, number, or silent rename.

### Base

**Base mirrors every Storage Action that takes an Entity**

- **Must** — Give Base one Action for every Storage Action that takes an Entity, in Storage's order and with its name.
- **Never** — Name or list an Action by hand, or add an Action that takes no Entity.

**Every Action works only through Storage Interface**

- **Must** — Call every Storage Action through Storage Interface with the one Storage access Base holds.
- **Never** — Reach Database or a Storage implementation detail from an Action.

**Every Action keeps to its bound Entity**

- **Must** — Reject an instance of another Entity with the Invalid Input error before calling Storage.
- **Never** — Check Field values.

### Entities

**Every Entity has exactly one Child Service**

- **Must** — Provide one Child Service for every Entity in Model's Entity Collection.
- **Never** — Copy or redefine an Entity.

**A Child Service holds only what is its own**

- **Must** — Keep only Entity-specific Behaviour or Actions in a Child Service.
- **Never** — Detach a Child Service from Base.

### Review

**Entity conformance covers every Entity contract**

- **Must** — show that the Interface needs, the Logic Entity Interface Schema, and the real Interface all match before Entity Service is conformant.
- **Never** — change anything outside Entity Service during review.

**Review observes Entity Service through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.

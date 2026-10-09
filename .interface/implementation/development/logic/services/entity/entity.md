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
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Entity Service is a fixed internal Service of every Logic Component. For every Entity in Model's Entity Collection it provides one Child Service, so a caller selects an Entity once and then calls its Actions without passing the Entity again. Its Interface publishes Service, the Child Services; Model, the Entity each binds; and, unchanged, the four Database groups Storage republishes.

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
- **Interface contract** — the versioned public contract of Entity Service Interface, stated in its Architecture section, with its version in Entity Service Preferences.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Entity Service
├── Interface
├── Base
├── Entities
└── Documentation
```

Every entity below is declared in `architecture` in Entity Service Preferences, which also own the configurable name, naming patterns, language, realization, and documentation choices; these selections realize the responsibilities below without changing them.

<!-------------------------- Interface -->
### Interface

```text
Interface
├── Service
├── Model
├── database_value
├── database_instance
├── database_result
└── database_error
```

The gateway callers import from: everything a caller needs to call Actions, build requests, read results, and catch errors without importing Model, Storage, or Database. It publishes its own two groups, Service and Model, named in Entity Service Preferences, and the four groups Storage republishes, and nothing else. Its Interface contract is these needs, with `contract_version` in Entity Service Preferences:

1. **Service** — exactly one Child Service for every Entity in Model's Entity Collection, changing when the Collection changes.
2. **Model** — the Entity every Child Service binds, under the same name as its Child Service, as the original object Model Interface publishes, never a copy, so no caller has to reach Model directly.
3. **Storage groups** — the four Database groups Storage Interface republishes, `database_value`, `database_instance`, `database_result`, and `database_error`, each passed on under its own name as the identical object, never a copy or a member taken out on its own, and read from Storage Interface each time rather than listed by hand.
4. **Nothing else** — Base, the Storage gateway, and anything beyond these groups are never published; Interface runs no check, and loading it opens no connection and creates no data or file.
5. **Versioned** — changing this structure requires raising `contract_version` and a consumer review; a change in Model's Entity Collection or in what Storage Interface publishes flows through without one.

For example, a caller creates `Service.User()`, calls `add` with a `Model.User`, filters `list` with a `database_value.Filter` on `Model.User.is_active`, and catches `database_error.InvalidInputError` when it passes a `Model.Account` instead.

<!-------------------------- Base -->
### Base

The layer that holds the one shared structure, in one unit, and every Action. When it is created, it takes one access to Storage, and every Action uses that same access. For every Storage Action that takes an Entity, in the order Storage publishes them, it offers one Action with the same name and the same parameters, except that a parameter taking the Entity class is removed and supplied from the bound Entity; a parameter taking an Entity instance stays. The Action hands the request to Storage and returns its answer and errors unchanged, with one exception: an instance that is not of the bound Entity is rejected with the Invalid Input error Storage Interface republishes, before Storage is called. Base reads only what Storage Interface publishes, located from Storage Service's own Preferences; each Action keeps its Storage Action's name with no prefix, and its parameters' names, order, and defaults.

<!-------------------------- Entities -->
### Entities

```text
Entities
└── one Child Service per Entity
```

The layer that holds one unit and one Child Service for every Entity in Model's Entity Collection. Each Child Service receives Base, binds its own Entity, and holds only Behaviour or Actions specific to that Entity. Their unit and structure names follow the Child naming patterns in Entity Service Preferences, and an override of a Base Action applies to its own Entity only.

<!-------------------------- Documentation -->
### Documentation

```text
Documentation
├── Overview
├── Interface
├── Use
└── Verify
```

The documentation of Entity Service, in the file, location, and format Entity Service Preferences name. Its sections, in this order:

1. **Overview** — What Entity Service is and why it exists, in one paragraph, with one simple example.
2. **Interface** — Every group with its members — every Child Service and its Actions, every Model, and every member of the four Storage groups — each with one example.
3. **Use** — How a caller imports a Child Service and how a Child Service adds its own Behaviour.
4. **Verify** — How to see that Entity Service matches Model's Entity Collection and Storage Interface.

<!-------------------------- Directory Structure -->
### Directory Structure

```text
Directory Structure
├── interface
├── base
├── entity/
└── README
```

The root of this tree is the Entity Service directory, named in `settings` in Entity Service Preferences. `entity/` holds one unit per Entity, named by the Child naming pattern.

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

#### Entity Service Interface conforms to the Interface contract

**Rule:** Every realization of Entity Service Interface conforms to the versioned Interface contract, which fixes its groups, the Actions of every Child Service, and what it never publishes.
**Why:** Every caller depends on one exact gateway instead of reinterpreting each realization.
**Boundary:** Changing the structure itself requires raising `contract_version`.

#### Entity Service names are valid and unique

**Rule:** The configured Service name, the Base name, the Service and Model group names, and every Child Service unit and structure name derived from the configured patterns are valid for the selected language and never collide within the same group. A Child Service and its Model share one name by design.
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

**Rule:** Entity Service is conformant only when its Interface contract and its real Interface match one another.
**Why:** A gap or a change here silently breaks every caller of Entity Service.
**Boundary:** Review reads Model and Storage Interfaces only to compare; it changes nothing outside Entity Service.

#### Review observes Entity Service through a fixed set of checks

**Rule:** Review establishes Entity conformance through these observations, every one of them on every review:
- Entity Service Interface publishes exactly Service, with one Child Service for every Entity in Model's Entity Collection; Model, with the Entity each Child Service binds under the same name; and the four groups Storage Interface republishes; and nothing else.
- Every object in Model and every republished group is the identical object its source Interface publishes.
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

**Entity Service Interface conforms to the Interface contract**

- **Must** — Conform every realization to the Interface contract.
- **Never** — Publish anything the contract does not list or change its structure without raising `contract_version`.

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

- **Must** — show that the Interface contract and the real Interface match before Entity Service is conformant.
- **Never** — change anything outside Entity Service during review.

**Review observes Entity Service through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.

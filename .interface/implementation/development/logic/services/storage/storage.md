# Storage Service Definition

Storage Service is the fixed internal Logic Service whose Interface gives other Logic Services access to every Operation of Database's Interface group.

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

Storage Service is a fixed internal Service of every Logic Component. It is Logic's complete gateway to Database: for every Operation of Database's Interface group, its one Storage gateway provides one corresponding Action. Its Interface publishes that gateway and republishes, unchanged, the Database groups those Actions need.

### Purpose

Logic Services need one controlled route to persistence, so that no Service reaches Database by its own way and Database internals stay hidden.

### How It Works

A Logic Service calls an Action on Storage; Storage hands the request to Database and returns Database's answer unchanged.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Storage Role** — the fixed identity of this Service inside Logic, independent of its configurable name.
- **Action** — one operation of the Core gateway, named and shaped exactly like one Operation of Database's Interface group.
- **Interface contract** — the versioned public contract of Storage Service Interface, stated in its Architecture section, with its version in Storage Service Preferences.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Storage Service
├── Interface
├── Core
└── Documentation
```

Every entity below is declared in `architecture` in Storage Service Preferences, which also own the configurable name, language, realization, and documentation choices; these selections realize the responsibilities below without changing them.

<!-------------------------- Interface -->
### Interface

```text
Interface
├── Storage
├── database_value
├── database_instance
├── database_result
└── database_error
```

The gateway other Logic Services import from. It publishes the Core gateway and, unchanged, the four Database groups a Service needs to build a request, read a result, and catch an error, so no Service has to reach Database directly. Its Interface contract is these needs, with `contract_version` in Storage Service Preferences:

1. **Complete** — exactly one Action for every Entity Operation and Command Operation in Database's Interface group, in the order Database publishes them, changing automatically when that group changes, so Storage never falls behind Database. Database's Setup group is not part of Storage.
2. **Unchanged** — every Action passes the Database Operation's input, result, and errors through exactly, so Database stays the only authority for storage.
3. **Needed contracts** — Database's Value, Instance, Result, and Error groups, each republished under Database's own group name as the identical object, never a copy or a member taken out on its own, and read from Database Interface each time rather than listed by hand.
4. **No behaviour** — no Action adds validation, retry, Engine or default-Instance selection, or a rule of its own, because behaviour belongs to the calling Service.
5. **Nothing else** — Action implementations, Database internals, and anything beyond these are never published; Interface runs no check, and loading it opens no connection and creates no data or file.
6. **Versioned** — changing this structure requires raising `contract_version` and a consumer review; a change in what Database Interface publishes flows through without one.

For example, a Service creates `Storage()`, calls `add` with a Model Entity, filters `list` with a `database_value.Filter` and selects `database_instance.SQLITE`, and catches `database_error.ConnectionFailureError`.

<!-------------------------- Core -->
### Core

The layer that holds the one gateway structure, in one unit, and every Action. Core reads only what Database Interface publishes, located from Database's own Preferences, never Database's structure files. When the gateway is created, it creates one object of Database's Interface group, and every Action uses that same object. For every Operation that group publishes, in the order Database publishes them, it offers one Action with exactly the Operation's name, no prefix, and the same parameter names, order, and defaults; the Action forwards every argument unchanged, performs no other work, and returns the Operation's answer and errors unchanged.

<!-------------------------- Documentation -->
### Documentation

```text
Documentation
├── Overview
├── Interface
├── Use
└── Verify
```

The documentation of Storage Service, in the file, location, and format Storage Service Preferences name. Its sections, in this order:

1. **Overview** — What Storage is and why it exists, in one paragraph, with one simple example.
2. **Interface** — Every Action and every republished contract, each with one example.
3. **Use** — How another Logic Service imports from the Storage Interface.
4. **Verify** — How to see that Storage has one Action for every Operation of Database's Interface group and republishes Database's four groups unchanged.

<!-------------------------- Directory Structure -->
### Directory Structure

```text
Directory Structure
├── interface
├── core
└── README
```

The root of this tree is the Storage Service directory, named in `settings` in Storage Service Preferences.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Database** — uses every Operation of Database's Interface group and its Value, Instance, Result, and Error groups, only through Database Interface. It finds that Interface from Database's own Preferences and never reads Database's structure files.
- **Consumes Development** — follows its shared rules and Defaults for every choice this Component leaves unstated.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Convenience and domain-specific Behaviour** — are not Storage's, because Storage is a raw gateway that adds no Behaviour.
- **Operation execution, Engine selection, connections, transactions, and result production** — are not Storage's, because Storage only requests published capabilities.
- **Capability meaning, membership, and validity** — are not Storage's, because Storage mirrors capabilities without defining them.
- **Publishing Services from Logic's root** — is not Storage's, because Storage owns only its own Interface.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Storage Service. Storage Service Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning and applicable Logic Principles retain their authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### Storage Service is fixed and internal

**Rule:** Every Logic contains the fixed Storage Role and its Interface. Its configured name may change, but its Role and responsibilities do not. Its implementation remains internal in every case.
**Why:** Logic needs one stable and discoverable Database gateway without confusing the Service with the Database Component or exposing implementation files.
**Boundary:** Its implementation and Database internals are never exposed.

<br>

### Interface

#### Storage Service Interface conforms to the Interface contract

**Rule:** Every realization of Storage Service Interface conforms to the versioned Interface contract, which fixes its Actions, their parameters, results, and errors, the republished groups, and what it never publishes.
**Why:** Every Logic Service depends on one exact gateway instead of reinterpreting each realization.
**Boundary:** Changing the structure itself requires raising `contract_version`.

#### Storage Service name is valid and unique

**Rule:** The configured Service name is valid for the selected language and never collides with a republished group.
**Why:** The gateway is named by it, and an invalid or colliding name cannot be realized safely.
**Boundary:** An invalid, reserved, or colliding value stops generation with a clear configuration error. The generator never invents a suffix, number, or silent rename.

<br>

### Core

#### Every Action is named exactly as its Database capability

**Rule:** Every Action has exactly the name of its Database capability, with no prefix or change. No Action is renamed by hand.
**Why:** Storage mirrors Database one to one, so whoever knows Database already knows Storage.
**Boundary:** The name identifies the Storage Action; it never renames or alters the Database capability.

#### Every Action works only through Database Interface

**Rule:** Every Action handles its Database capability only by calling that capability through Database Interface, using the one Database access the Core gateway took when it was created.
**Why:** One route keeps every Action a faithful mirror of Database and keeps Database's internals out of Logic.
**Boundary:** An Action never reaches a Database implementation detail.

<br>

### Review

#### Storage conformance covers every Storage contract

**Rule:** Storage Service is conformant only when its Interface contract and its real Interface match one another.
**Why:** A gap or a change here silently breaks every caller of Storage.
**Boundary:** Review reads Database Interface only to compare; it changes nothing outside Storage Service.

#### Review observes Storage through a fixed set of checks

**Rule:** Review establishes Storage conformance through these observations, every one of them on every review:

- Storage Service Interface publishes exactly one Action for every Operation of Database's Interface group, Database's Value, Instance, Result, and Error groups, and nothing else.
- Each Action has the same parameter names, order, and defaults as its Database capability.
- Each Action returns its Database capability's result and raises its errors unchanged.
- Every republished group is the identical object Database Interface publishes.
- No Action adds validation, retry, Engine or default-Instance selection, or a rule of its own.
- Every Action is an operation of the one Core gateway, has exactly its Database capability's name, and uses the one Database access that gateway holds.
- Loading the Interface opens no connection and creates no data or file.

**Why:** A fixed set of observations proves the same things on every review, so a result is never judged by a different standard from one run to the next.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it; how it is realized belongs to the Review Operation.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Storage Service is fixed and internal**

- **Must** — Include the Storage Role and its Interface in every Logic.
- **Never** — Expose its private implementation or confuse its configurable name with its fixed Role.

<br>

### Interface

**Storage Service Interface conforms to the Interface contract**

- **Must** — Conform every realization to the Interface contract.
- **Never** — Publish anything the contract does not list or change its structure without raising `contract_version`.

**Storage Service name is valid and unique**

- **Must** — Keep the configured Service name valid and free of collision with every republished group.
- **Never** — Resolve a collision by inventing a suffix, number, or silent rename.

<br>

### Core

**Every Action is named exactly as its Database capability**

- **Must** — Give every Action exactly its Database capability's name.
- **Never** — Rename an Action by hand.

**Every Action works only through Database Interface**

- **Must** — Handle every Database capability through Database Interface with the one Database access the Core gateway holds.
- **Never** — Reach a Database implementation detail from an Action.

<br>

### Review

**Storage conformance covers every Storage contract**

- **Must** — show that the Interface contract and the real Interface match before Storage is conformant.
- **Never** — change anything outside Storage Service during review.

**Review observes Storage through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.

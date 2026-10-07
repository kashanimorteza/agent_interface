# Storage Service Definition

Storage Service is the fixed internal Logic Service whose Interface gives other Logic Services access to every public capability published by Database.

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

Storage Service is a fixed internal Service of every Logic Component. It is Logic's complete gateway to Database: for every capability Database Interface publishes, its one Storage gateway provides one corresponding Action. Its Interface publishes that gateway and republishes the Database contracts those Actions need.

### Purpose

Logic Services need one controlled route to persistence, so that no Service reaches Database by its own way and Database internals stay hidden.

### How It Works

A Logic Service calls an Action on Storage; Storage hands the request to Database and returns Database's answer unchanged.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Storage Role** — the fixed identity of this Service inside Logic, independent of its configurable name.
- **Action** — one operation of the Core gateway, named and shaped exactly like one capability published by Database Interface.
- **Logic Storage Interface Schema** — the versioned structure that fixes the exact shape of Storage Service Interface.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Storage Service
├── Interface   ← the gateway, in the shape the Logic Storage Interface Schema defines
└── Core        ← the gateway structure that offers every Action
```

Storage Service Preferences own its configurable name, directory, architecture, language and realization, and documentation. The shape of its Interface belongs to the Logic Storage Interface Schema.

### Interface

The gateway other Logic Services import from. It publishes the Core gateway and the Database contracts it needs. It meets these needs:

1. **Complete** — exactly one Action for every capability Database Interface publishes, changing automatically when Database's capabilities change, so Storage never falls behind Database.
2. **Unchanged** — every Action passes the Database capability's input, result, and errors through exactly, so Database stays the only authority for storage.
3. **Needed contracts** — everything a Service needs to build a request, read a result, and catch an error is republished as the original object, never a copy, so no Service has to reach Database directly.
4. **No behaviour** — no Action adds validation, retry, Engine or default-Instance selection, or a rule of its own, because behaviour belongs to the calling Service.
5. **Nothing else** — nothing beyond these is published, and loading the Interface has no side effect.

The exact shape of these needs is fixed by the Logic Storage Interface Schema, which is built from them. These needs are the reference: when the two differ, the Schema is corrected to match them.

### Core

The layer that holds the one gateway structure, in one unit, and every Action. When the gateway is created, it takes one access to Database, and every Action uses that same access. For every capability Database Interface publishes, in the order Database publishes them, it offers one Action with the same name and the same parameters; the Action hands the request to that capability and returns its answer.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Database** — uses every capability and supporting contract Database Interface publishes, only through Database Interface. It finds that Interface from Database's own Preferences and never reads Database's structure files.
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

#### Storage Service Interface conforms to the Logic Storage Interface Schema

**Rule:** Every realization of Storage Service Interface conforms to the versioned Logic Storage Interface Schema, which fixes its Actions, their parameters, results, and errors, the republished contracts, and what it never publishes.
**Why:** Every Logic Service depends on one exact gateway instead of reinterpreting each realization.
**Boundary:** Changing the structure itself requires a Schema version change.

#### Storage Service name is valid and unique

**Rule:** The configured Service name is valid for the selected language and never collides with a republished contract.
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

**Rule:** Storage Service is conformant only when its Interface needs in this Definition, the Logic Storage Interface Schema, and its real Interface all match one another.
**Why:** A gap or a change here silently breaks every caller of Storage.
**Boundary:** Review reads Database Interface only to compare; it changes nothing outside Storage Service.

#### Review observes Storage through a fixed set of checks

**Rule:** Review establishes Storage conformance through these observations, every one of them on every review:

- Every need of the Interface and Core layers in this Definition appears in the Logic Storage Interface Schema, and the Schema holds nothing beyond them.
- Storage Service Interface publishes exactly one Action for every capability Database Interface publishes, and nothing else.
- Each Action has the same parameter names, order, and defaults as its Database capability.
- Each Action returns its Database capability's result and raises its errors unchanged.
- Every republished contract, including every Database error, is the identical object Database Interface publishes.
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

**Storage Service Interface conforms to the Logic Storage Interface Schema**

- **Must** — Conform every realization to the Logic Storage Interface Schema.
- **Never** — Publish anything the Schema does not list or change its structure without a Schema version change.

**Storage Service name is valid and unique**

- **Must** — Keep the configured Service name valid and free of collision with every republished contract.
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

- **Must** — show that the Interface needs, the Logic Storage Interface Schema, and the real Interface all match before Storage is conformant.
- **Never** — change anything outside Storage Service during review.

**Review observes Storage through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.

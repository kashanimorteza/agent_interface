# Logic Definition

Logic is the Development Component that holds the application's Behaviour in modular Services and publishes every Service Interface through one Interface.

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

Logic is the reusable library that holds the application's Services. It has nothing of its own: its Interface publishes every Service's Interface under that Service's name.

### Purpose

Consumers need one place to find every Service, so that none of them depends on where a Service lives inside Logic.

### How It Works

A consumer imports Logic Interface, selects a Service, and uses what that Service publishes.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Service** — one modular part of Logic that owns one coherent responsibility, all of its files in its own directory, and its own Interface, Definition, and Preferences.
- **Service Interface** — the gateway inside one Service's directory that presents that Service's capabilities.
- **Logic Interface Schema** — the versioned structure that fixes the exact shape of Logic Interface.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Logic
├── Interface       ← every Service Interface, in the shape the Logic Interface Schema defines
└── Services        ← one directory per Service
```

Logic Preferences own its identity, architecture, Service list, language and realization, and documentation. The shape of its Interface belongs to the Logic Interface Schema.

### Interface

Logic's outward surface. It meets these needs:

1. **Complete** — exactly one entry for every Service listed in Logic Preferences, under that Service's configured name, changing when the list changes.
2. **Unchanged** — each entry is that Service's own Interface, never a copy, wrapper, or added Action.
3. **Nothing else** — nothing beyond these is published.

The exact shape of these needs is fixed by the Logic Interface Schema, which is built from them. These needs are the reference: when the two differ, the Schema is corrected to match them.

### Services

Every Service listed in Logic Preferences has its own directory and Interface, and is governed by its own Definition and Preferences.

#### Entity Service

One Child Service for every Model Entity.

→ [Definition of Entity Service](services/entity/entity.md)<br>
→ [Preferences of Entity Service](services/entity/entity.yaml)

#### Storage Service

Logic's gateway to Database.

→ [Definition of Storage Service](services/storage/storage.md)<br>
→ [Preferences of Storage Service](services/storage/storage.yaml)

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Development** — takes its identity, its technology, and the Connections it is permitted to make.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Behaviour and Actions** — are not Logic's, because every Action is defined and implemented by the Service that owns it.
- **A Service's own contract** — is not Logic's, because that Service's Definition and Preferences decide it.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Every Principle in this file is mandatory for Logic and every Logic Service. Logic Preferences provide configurable defaults and conventions but can never weaken a Principle. Explicit Target meaning and each Service's own Principles retain their authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### Logic is a reusable library

**Rule:** Logic exposes Behaviour only through its Interface. It starts no process, owns no transport schema, and depends on no consumer's framework.
**Why:** Behaviour without a transport of its own can be reused by any consumer and tested without a running server.
**Boundary:** Being a library never makes a Service's implementation public.

### Interface

#### Logic Interface conforms to the Logic Interface Schema

**Rule:** Every realization of Logic Interface conforms to the versioned Logic Interface Schema, which fixes what it publishes and what it never publishes.
**Why:** Every consumer depends on one exact gateway instead of reinterpreting each realization.
**Boundary:** Changing the structure itself requires a Schema version change.

#### Service imports point away from Logic Interface

**Rule:** Logic Interface imports Service Interfaces; no Service ever imports Logic Interface. A Service that collaborates with another imports that Service's Interface directly.
**Why:** One-way imports keep Logic Interface and its Services free of a dependency cycle.
**Boundary:** A direct Service Interface import is collaboration inside Logic, never an external entry point.

#### Service names are unique within Logic

**Rule:** No two Services share a name or a directory.
**Why:** Logic Interface cannot publish two Services under one name.
**Boundary:** A collision stops generation with a clear configuration error; nothing is renamed silently.

### Services

#### Logic is composed of modular Services

**Rule:** All of Logic's work is divided into Services, each owning one coherent responsibility, its own directory, and its own Interface. Entity Service and Storage Service are fixed in every Logic; more Services may be added.
**Why:** One Service per responsibility keeps its dependencies and Behaviour together, so a change stays inside it.
**Boundary:** Services sit beside one another; a Service uses another only through that Service's Interface.

#### Storage Service is every other Service's only route to Database

**Rule:** Every Logic Service that needs Database uses Storage Service Interface; only Storage Service calls Database Interface.
**Why:** One gateway keeps Database access consistent and replaceable across Logic.
**Boundary:** A Service owns any Behaviour it adds around a Storage call.

### Review

#### Logic conformance covers every Logic contract

**Rule:** Logic is conformant only when its Interface needs in this Definition, the Logic Interface Schema, and its real Interface all match one another.
**Why:** A gap here silently hides or misnames a Service for every consumer.
**Boundary:** Review reads Service Interfaces only to compare; it changes nothing outside Logic's own files.

#### Review observes Logic through a fixed set of checks

**Rule:** Review establishes Logic conformance through these observations, every one of them on every review:
- Every need of the Interface layer in this Definition appears in the Logic Interface Schema, and the Schema holds nothing beyond them.
- Logic Interface publishes exactly one entry for every Service listed in Logic Preferences, under its configured name, and nothing else.
- Every entry is the identical Interface object of its Service.
- No Service other than Storage Service imports Database Interface.
- No Service imports Logic Interface.
- No two Services share a name or directory.
**Why:** A fixed set of observations proves the same things on every review, so a result is never judged by a different standard from one run to the next.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it; how it is realized belongs to the Review Operation.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Logic is a reusable library**

- **Must** — Expose Behaviour only through Logic Interface.
- **Never** — Start a process, own a transport schema, or depend on a consumer's framework.

### Interface

**Logic Interface conforms to the Logic Interface Schema**

- **Must** — Conform every realization to the Logic Interface Schema.
- **Never** — Publish anything the Schema does not list or change its structure without a Schema version change.

**Service imports point away from Logic Interface**

- **Must** — Import Service Interfaces into Logic Interface, and another Service's Interface directly when collaborating.
- **Never** — Import Logic Interface from a Service.

**Service names are unique within Logic**

- **Must** — Keep every Service name and directory unique within Logic.
- **Never** — Resolve a collision by a silent rename.

### Services

**Logic is composed of modular Services**

- **Must** — Divide all of Logic's work into Services, each with its own directory and Interface, including Entity and Storage Service.
- **Never** — Let one Service reach into another except through its Interface.

**Storage Service is every other Service's only route to Database**

- **Must** — Use Storage Service Interface whenever a Service needs Database.
- **Never** — Call Database Interface from any Service but Storage Service.

### Review

**Logic conformance covers every Logic contract**

- **Must** — show that the Interface needs, the Logic Interface Schema, and the real Interface all match before Logic is conformant.
- **Never** — change anything outside Logic's own files during review.

**Review observes Logic through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.

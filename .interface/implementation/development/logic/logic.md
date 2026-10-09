# Logic Definition

Logic is the Development Component that holds the application's Behavior in modular Services and publishes every Service Interface through one Interface.

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
- **Interface contract** — the versioned public contract of Logic Interface, stated in its Architecture section, with its version in Logic Preferences.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Logic
├── Interface
├── Services
└── Documentation
```

Every entity below is declared in `architecture` in Logic Preferences, which also own the language, realization, and documentation choices; these selections realize the responsibilities below without changing them.

<!-------------------------- Interface -->
### Interface

Logic's outward surface: one entry for every Service, under that Service's name. Interface lives in its own `interface` file, the only file that publishes; the package's own initialiser, where the language has one, publishes nothing. Its Interface contract is these needs, with `contract_version` in Logic Preferences:

1. **Complete** — exactly one entry for every Service listed in Logic Preferences, under that Service's configured name, changing when the list changes; each Service's name and Interface location come from that Service's own Preferences.
2. **Unchanged** — each entry is that Service's own Interface, the identical object, never a copy, wrapper, or added Action.
3. **Nothing else** — nothing beyond these is published, and Interface defines no Action, wrapper, or rule of its own and runs no check.
4. **Versioned** — changing this structure requires raising `contract_version` and a consumer review; adding or removing a Service in the list flows through without one.

For a Logic with Entity Service, Interface publishes `Entity`, the identical Interface of that Service.

<!-------------------------- Services -->
### Services

```text
Services
└── Entity Service
```

Every Service listed in Logic Preferences has its own directory and Interface, and is governed by its own Definition and Preferences.

#### Entity Service

One Child Service for every Model Entity.

→ [Definition of Entity Service](services/entity/entity.md)
→ [Preferences of Entity Service](services/entity/entity.yaml)

<!-------------------------- Documentation -->
### Documentation

```text
Documentation
├── Overview
├── Interface
├── Services
├── Setup
├── Use
├── Verify
└── Troubleshooting
```

The root documentation, in the file, location, and format Logic Preferences name. Its sections, in this order:

1. **Overview** — What Logic is and why it exists, in one paragraph, with one simple example.
2. **Interface** — Every name Logic Interface publishes.
3. **Services** — For every Service, its name and links to its README, its Definition, and its Preferences; never a copy of its contract.
4. **Setup** — How to install Logic and what it needs next to it.
5. **Use** — How a consumer imports from Logic Interface.
6. **Verify** — How to see that Logic Interface publishes exactly every listed Service.
7. **Troubleshooting** — Real problems a consumer can meet and how to fix them.

<!-------------------------- Directory Structure -->
### Directory Structure

```text
Directory Structure
├── logic/
│   ├── interface
│   └── services/
│       └── entity/
└── README
```

The root of this tree is the Component directory; it and the package directory take their names from `settings` in Logic Preferences. Each Service has its own directory under `services/`, named by the Service's key in Logic Preferences.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Development** — takes its identity, its technology, and the Connections it is permitted to make.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Behavior and Actions** — are not Logic's, because every Action is defined and implemented by the Service that owns it.
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

**Rule:** Logic exposes Behavior only through its Interface. It starts no process, owns no transport schema, and depends on no consumer's framework.
**Why:** Behavior without a transport of its own can be reused by any consumer and tested without a running server.
**Boundary:** Being a library never makes a Service's implementation public.

### Interface

#### Logic Interface conforms to the Interface contract

**Rule:** Every realization of Logic Interface conforms to the versioned Interface contract, which fixes what it publishes and what it never publishes.
**Why:** Every consumer depends on one exact gateway instead of reinterpreting each realization.
**Boundary:** Changing the structure itself requires raising `contract_version`.

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

**Rule:** All of Logic's work is divided into Services, each owning one coherent responsibility, its own directory, and its own Interface. Entity Service is fixed in every Logic; more Services may be added.
**Why:** One Service per responsibility keeps its dependencies and Behavior together, so a change stays inside it.
**Boundary:** Services sit beside one another; a Service uses another only through that Service's Interface.

#### Entity Service is every other Service's only route to Database

**Rule:** Every Logic Service that needs Database uses Entity Service Interface; only Entity Service calls Database Interface, and it never uses Database's Setup group or Command Operations.
**Why:** One gateway keeps Database access consistent and replaceable across Logic.
**Boundary:** A Service owns any Behavior it adds around an Entity Service call.

### Review

#### Logic conformance covers every Logic contract

**Rule:** Logic is conformant only when its Interface contract and its real Interface match one another.
**Why:** A gap here silently hides or misnames a Service for every consumer.
**Boundary:** Review reads Service Interfaces only to compare; it changes nothing outside Logic's own files.

#### Review observes Logic through a fixed set of checks

**Rule:** Review establishes Logic conformance through these observations, every one of them on every review:
- Logic Interface publishes exactly one entry for every Service listed in Logic Preferences, under its configured name, and nothing else.
- Every entry is the identical Interface object of its Service.
- No Service other than Entity Service imports Database Interface.
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

- **Must** — Expose Behavior only through Logic Interface.
- **Never** — Start a process, own a transport schema, or depend on a consumer's framework.

### Interface

**Logic Interface conforms to the Interface contract**

- **Must** — Conform every realization to the Interface contract.
- **Never** — Publish anything the contract does not list or change its structure without raising `contract_version`.

**Service imports point away from Logic Interface**

- **Must** — Import Service Interfaces into Logic Interface, and another Service's Interface directly when collaborating.
- **Never** — Import Logic Interface from a Service.

**Service names are unique within Logic**

- **Must** — Keep every Service name and directory unique within Logic.
- **Never** — Resolve a collision by a silent rename.

### Services

**Logic is composed of modular Services**

- **Must** — Divide all of Logic's work into Services, each with its own directory and Interface, including Entity Service.
- **Never** — Let one Service reach into another except through its Interface.

**Entity Service is every other Service's only route to Database**

- **Must** — Use Entity Service Interface whenever a Service needs Database.
- **Never** — Call Database Interface from any Service but Entity Service.

### Review

**Logic conformance covers every Logic contract**

- **Must** — show that the Interface contract and the real Interface match before Logic is conformant.
- **Never** — change anything outside Logic's own files during review.

**Review observes Logic through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.

# API Definition

API is the Development Component that publishes selected Logic capabilities through one external HTTP boundary composed of modular Groups.

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

API is the application's single external HTTP gateway. It owns the shared running boundary, composition, runtime-facing configuration contract, and common public contract. Its usable capability areas are modular Groups. Every Group owns its own external surface and explains how that surface is derived and realized.

API Definition and Preferences contain only concepts and defaults shared by the whole API. They do not define the contract of a particular Group. Each Group has its own Definition and Preferences under the configured Groups directory, and API references those files rather than copying their content.

API remains independent of programming language, framework, package, and implementation technique. API Preferences may choose a default realization; the selected package or implementation skill decides compatible technical mechanics without changing this contract.

### Purpose

External consumers need one stable boundary while different capability areas need independent ownership. API provides the shared boundary without turning its root into a catalogue of routes, Actions, schemas, or rules that belong to individual Groups.

This separation lets a Group evolve from its own contract while all Groups continue to share one API identity and lifecycle. Adding, changing, or removing a Group changes that Group and its reference, not the meaning of the root API Component.

### How It Works

API reads the Group references declared in API Preferences. Each referenced Group resolves its own source, eligibility, structure, external contract, and configurable defaults from its Definition and Preferences. API composes the resolved Groups into one running boundary.

Bootstrap starts and composes the API. Core contains only private capabilities shared across Groups. Configuration receives runtime values declared by API. Root documentation introduces the API and points consumers to the documentation of its enabled Groups.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **API Group** — one modular external capability area with its own Definition and Preferences under the Groups directory.
- **Group Reference** — the pair of paths through which API discovers one Group's Definition and Preferences without copying them.
- **Bootstrap** — the single composition and startup point that assembles the API and registers its resolved Groups.
- **Core** — the private home of capabilities shared by multiple Groups and owned by none of them.
- **External Contract** — the observable human- and machine-readable description of the running API boundary.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
API
├── bootstrap
├── core/
├── groups/
│   └── <group>/
├── config.yaml
└── README.md
```

The names shown are defaults selected by API Preferences. Every `<group>` directory contains that Group's independent Definition and Preferences; its internal realization is owned by those files.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Logic** — Groups reach the Logic capabilities their own contracts declare.
- **Consumes Development** — receives shared implementation defaults and declared Component connections.
- **Consumes Platform** — receives runtime bindings required by the running boundary.
- **Consumed by Presentation and external clients** — publishes one external HTTP boundary containing its enabled Groups.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Application Behaviour and decisions** — belong to Logic; API carries external requests without reimplementing them.
- **Domain meaning** — belongs to Model and is never read directly by API.
- **Persistence** — belongs behind Logic and Database; API never reaches it directly.
- **A particular Group's source, structure, routes, requests, responses, and failures** — belong to that Group's Definition and Preferences.
- **Capabilities shared by the complete external boundary** — belong to API.
- **Technical framework mechanics** — belong to the selected package and implementation skill when not explicitly selected by Target or compatible Preferences.
- **Runtime values and process operation** — are supplied by Platform; API declares only what the running boundary needs.
- **Authentication** — is absent from the current shared API contract and is never generated implicitly.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

API owns one shared composition. Bootstrap registers the referenced Groups, Core supports them privately, Configuration receives runtime values, and Documentation presents one coherent external boundary. A Group's own files define its internal layers and public capability contract.

### Bootstrap

The single composition and startup point. It resolves and registers every referenced Group, applies concerns shared by the whole API, and exposes one running boundary. It contains no Group capability or application Behaviour.

### Core

The private directory for API capabilities shared by multiple Groups and owned by none of them. A capability owned by one Group remains inside that Group.

### Groups

The configured directory containing modular API Groups. API references each Group's Definition and Preferences here and does not repeat the Group contract in root files.

### Entity Group

Entity Group is the initial API Group.

→ [Definition of Entity Group](groups/entity/entity.md)<br>
→ [Preferences of Entity Group](groups/entity/entity.yaml)

An additional Group follows the same modular rule: it receives its own directory, Definition, and Preferences, and API references it instead of copying its contract into root API files.

### Configuration

`config.yaml` contains only runtime values declared by the API boundary. Component structure and configurable defaults remain in API Preferences or the owning Group Preferences, while Platform supplies environment-specific bindings.

### Documentation

Root documentation introduces the API, its shared lifecycle, and its enabled Groups. The detailed capabilities of a Group are documented from that Group's own contract.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

API Definition Principles are mandatory for the shared boundary. API Preferences provide configurable defaults for unstated shared choices. Each Group Definition and Preferences govern that Group without weakening API Principles. Explicit compatible Target meaning takes precedence over defaults.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the category that owns it.

### General

#### API remains independent of its realization

**Rule:** API Definition fixes shared responsibilities, boundaries, composition, and observable contracts without requiring a programming language, framework, package, decorator, or implementation pattern.
**Why:** The same API Component must remain understandable and implementable across compatible technology choices.
**Boundary:** Preferences and the selected implementation skill may choose compatible mechanics but may not change the conceptual contract.

#### API is one external boundary

**Rule:** API has one Bootstrap, one running boundary, and one shared lifecycle for all referenced Groups.
**Why:** Groups are modular capability areas of one API, not separate applications merely because their contracts are independent.
**Boundary:** An explicit Target may define another API Component, but a Group never starts its own server or process.

<br>

### Groups

#### Groups are independently defined and referenced

**Rule:** Every API Group has its own Definition and Preferences inside its own directory. API root files contain only a reference to that pair and never copy the Group's source, layers, capabilities, routes, schemas, or configurable defaults.
**Why:** Each Group needs one authoritative contract that can evolve without enlarging or contradicting the root API contract.
**Boundary:** API may introduce and compose a referenced Group, but all details specific to that Group remain in its files.

#### Group references are complete and unique

**Rule:** Every configured Group identity is unique and resolves to exactly one existing Definition and one existing Preferences file under the configured Groups directory. Invalid, missing, stale, or colliding references stop generation with a clear error.
**Why:** API cannot compose a Group whose authority is ambiguous or incomplete.
**Boundary:** Generation never repairs a reference through an invented path, suffix, number, or silent rename.

<br>

### Bootstrap and Core

#### Bootstrap composes without owning Group capabilities

**Rule:** Bootstrap resolves and registers referenced Groups and applies only shared API concerns. It defines no Group capability, route, schema, application Behaviour, or persistence work.
**Why:** Composition stays stable while Groups retain authority over their own external surfaces.
**Boundary:** Registration mechanics belong to the selected realization; capability meaning remains in the owning Group.

#### Core remains shared and private

**Rule:** A private API capability shared by multiple Groups and owned by none belongs in Core. Core publishes no external capability and contains no application Behaviour.
**Why:** Shared concerns need one internal home without becoming another public layer.
**Boundary:** A Group-specific concern stays in that Group even when another Group has a similar concern.

<br>

### Contract and Documentation

#### API owns one consistent combined contract

**Rule:** Running behaviour, machine-readable contract, and human documentation describe the same enabled Groups and shared lifecycle.
**Why:** Consumers must not build against a description that differs from the running boundary.
**Boundary:** Each Group remains authoritative for its detailed portion of that combined contract.

#### Root documentation references Group documentation

**Rule:** Root documentation introduces every enabled Group and directs consumers to its generated contract without copying its detailed capabilities.
**Why:** Consumers need one overview while Group details retain one owner.
**Boundary:** Root documentation exposes no disabled Group or private implementation detail.

<br>

### Lifecycle and Verification

#### Health and readiness always exist

**Rule:** API always exposes distinct health and readiness signals. Health reports that the API is alive; readiness is positive only after required configuration and dependencies are ready. Their paths are configurable, but the signals cannot be disabled.
**Why:** Operators need to distinguish a running process from one able to serve requests.
**Boundary:** The selected package implements the signals, while Platform decides how to use them.

#### Verification covers shared composition

**Rule:** API verification confirms reference validity and uniqueness, successful Group composition, one shared lifecycle, contract consistency, and health and readiness signals. Each Group defines verification of its own detailed contract.
**Why:** Root verification should prove the combined boundary without duplicating Group verification.
**Boundary:** API verification never replaces Logic Behaviour, Group contract, or Database persistence verification.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**API remains independent of its realization**

- **Must** — Preserve shared responsibilities, boundaries, composition, and observable contracts across compatible realizations.
- **Never** — Make a language, framework, package, or implementation pattern part of API Definition.

**API is one external boundary**

- **Must** — Compose every referenced Group through one Bootstrap and lifecycle.
- **Never** — Let a Group create another server or process.

### Groups

**Groups are independently defined and referenced**

- **Must** — Give each Group its own Definition and Preferences and reference them from API.
- **Never** — Copy Group-specific structure, capabilities, routes, schemas, or defaults into root API files.

**Group references are complete and unique**

- **Must** — Resolve every unique Group identity to one valid Definition and Preferences pair.
- **Never** — Silently repair a missing, invalid, stale, or colliding reference.

### Bootstrap and Core

**Bootstrap composes without owning Group capabilities**

- **Must** — Register Groups and apply shared API concerns only.
- **Never** — Define a Group capability or application Behaviour in Bootstrap.

**Core remains shared and private**

- **Must** — Keep only shared private API capabilities in Core.
- **Never** — Publish Core or move a Group-owned concern into it.

### Contract and Documentation

**API owns one consistent combined contract**

- **Must** — Keep the running boundary and both contract forms consistent.
- **Never** — Let composition contradict an owning Group's contract.

**Root documentation references Group documentation**

- **Must** — Introduce enabled Groups and direct consumers to their contracts.
- **Never** — Duplicate Group details or expose disabled Groups.

### Lifecycle and Verification

**Health and readiness always exist**

- **Must** — Expose distinct configurable health and readiness signals.
- **Never** — Disable either signal or report readiness prematurely.

**Verification covers shared composition**

- **Must** — Verify references, composition, lifecycle, combined contract, health, and readiness.
- **Never** — Duplicate or replace verification owned by a Group, Logic, or Database.

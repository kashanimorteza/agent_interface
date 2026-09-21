# Launch Definition

Launch is the Operation Component that activates a completed implementation and records the observable runtime result.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Layering](#layering)**
5. **[Authority](#authority)**
6. **[Principles](#principles)**
7. **[Operation Contract](#operation-contract)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Launch is the Operation Component that brings a completed implementation online and records the observable runtime result.

### Purpose

A completed implementation is not the same as a safely running one. Launch provides the bounded operation that validates readiness, activates the runtime, and preserves the result.

### How It Works

Launch reads the applicable Platform and operational authorities, verifies readiness, performs the authorized activation, observes the result, and records success, failure, or the need for human action.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Launch Result** — the observable outcome of activating the implementation.
- **Readiness** — the state in which the implementation and its required dependencies may be activated safely.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Development and Platform authorities** — uses the completed product and its launch requirements.
- **Consumes State** — reads the current operational position and records the launch outcome through its owner.
- **Consumed by State** — supplies the observable runtime result.

<br>

Launch owns activation and observation, not product Source, Platform definitions, or runtime secrets.

Every Principle in this file is mandatory. An Operations Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Launch owns activation and its observable result. Development owns the implementation, Platform owns runtime capability, and State owns the recorded Launch State.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principle and Operation Contract in this Definition govern Launch. Launch Preferences supply only activation defaults where higher authorities are silent.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Launch activates only a ready implementation

**Rule:** Launch verifies the applicable readiness conditions before activation, exposes no secret values, and records the observable runtime result and any required human action.

**Why:** Activation without readiness turns an implementation failure into an uncontrolled runtime failure.

**Boundary:** Launch never changes Target meaning, product Source, or Platform authority to make an activation appear ready.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
<!--------------------------------------------------------------------------------- Operation Contract --->
## Operation Contract

Launch accepts one optional scope: `api`, `presentation`, `logic`, or `complete` (`all` is an alias). With no scope, it asks the Human to choose one. It consumes Target and Platform selections, Platform authorities, State, developed parts, public interfaces, and observable runtime state.

Launch establishes current Interface and Target Understanding, reads Platform Principles and Preferences and operational State, and resolves the Environment and Launch definition from explicit Target decisions before Platform defaults. It never invents a missing definition.

Launch prepares only declared project-scoped runtime requirements, verifies readiness, activates only the selected parts in dependency order, preserves already healthy parts, delivers bindings through public boundaries without recording secrets, and records startup or preservation outcomes, readiness evidence, Access Points, Launch State and History, Blockers, and Open Questions.

Launch never repairs product Source, changes Target meaning, redefines Platform authority, or exposes secrets. It stops on unresolved Environment or Launch, missing system preparation, failed preparation or prerequisite startup, incomplete Development, failed readiness, or an unsafe binding.

Launch is idempotent: a healthy running part is preserved and only runtime elements that do not satisfy the current scope are changed.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Launch activates only a ready implementation**

- **Must** — verify readiness and record the observable runtime result.
- **Never** — alter product or Platform authority to bypass a readiness failure.

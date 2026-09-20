# Agent Skill Definition

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Shared Guidance](#shared-guidance)**
   - **[Each Skill layer has one owner](#each-skill-layer-has-one-owner)**
   - **[Every Skill has one Contract](#every-skill-has-one-contract)**
   - **[Skill availability is proven](#skill-availability-is-proven)**
   - **[Skill execution is repeatable](#skill-execution-is-repeatable)**
   - **[Every Skill has one Realization Kind](#every-skill-has-one-realization-kind)**
   - **[Skill owns executable capability only](#skill-owns-executable-capability-only)**
5. **[At a Glance](#at-a-glance)**




<br><br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Skill is a reusable capability an Agent can activate to perform a defined kind of work.

### Purpose

Skill prevents the Agent from reconstructing the same instructions each time. Each Skill has one responsibility and one portable Contract.

### How It Works

The Contract is the authoritative source for one Skill's behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions. Agent Sync carries the Contract into the selected Runtime, where the Runtime owns execution mechanics. A prepared file or an external provider can supply a different realization, but neither changes the Contract's meaning.




<br><br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Skill** — a reusable capability activated explicitly or by a declared coordinator.
- **Skill Contract** — the authoritative definition of one Skill's behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions.
- **Capability Realization Kind** — the declared way a Skill becomes usable: Constructed from a Contract, Prepared from declared content, or Installed through a provider.




<br><br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Agent, Implementation, and Target** — reads the authorities required by its Contract.
- **Consumed by Agent and permitted Coordinators** — provides an executable capability without acquiring the authority of its sources.
- **Realized by Agent Sync** — is carried into the selected Runtime without changing its Contract.




<br><br>

<!--------------------------------------------------------------------------------- Shared Guidance --->
## Shared Guidance

### Each Skill layer has one owner

**Rule:** This Guide explains the shared Skill concept, each Contract owns Skill-specific behavior, and the selected Runtime owns execution mechanics.

**Why:** Clear ownership prevents duplication and conflicting authorities.

**Boundary:** No layer replaces, overrides, or duplicates another layer's authority.


### Every Skill has one Contract

**Rule:** Every Interface-owned Skill has one complete Contract.

**Why:** One Contract keeps each Skill's behavior clear and consistent.

**Boundary:** This Guide does not repeat a Skill Contract or define one Skill's workflow.


### Skill availability is proven

**Rule:** A Skill is usable only when the selected Runtime can discover and invoke it.

**Why:** A declaration alone does not make a capability available.

**Boundary:** Invocation never expands the Skill's authority or responsibility.


### Skill execution is repeatable

**Rule:** Repeating a Skill preserves valid work and avoids unnecessary changes.

**Why:** Skills may be resumed or invoked more than once.

**Boundary:** Repeatability never authorizes destructive replacement of meaningful work.


### Every Skill has one Realization Kind

**Rule:** Each Skill has one realization path: Constructed, Prepared, or Installed.

**Why:** The Runtime needs one clear realization path for every Skill.

**Boundary:** Realization never changes the Contract's meaning or authority.


### Skill owns executable capability only

**Rule:** A Skill owns its executable capability and does not own Target meaning, Implementation policy, Runtime mechanics, or another Component's records.

**Why:** Clear ownership keeps reusable capability separate from the authorities it consumes.

**Boundary:** A Skill may read required authorities and produce its declared outputs without acquiring ownership of them.




<br><br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

**Each Skill layer has one owner** — Guide explains the shared concept; Contract owns Skill behavior; Runtime owns execution mechanics.

**Every Skill has one Contract** — define each Interface-owned Skill through one authoritative Contract.

**Skill availability is proven** — verify Runtime discovery and invocation; never infer availability from declaration alone.

**Skill execution is repeatable** — preserve valid work on repetition; never replace meaningful work destructively.

**Every Skill has one Realization Kind** — use exactly one of Constructed, Prepared, or Installed.

**Skill owns executable capability only** — keep ownership limited to the declared capability.

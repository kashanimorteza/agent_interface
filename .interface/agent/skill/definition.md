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

Skill prevents the Agent from reconstructing the same instructions each time. Each Process-backed Skill points to one owning Process Component, whose Definition and Preferences contain the meaning the Skill executes; Agent Skill Preferences contain only the Agent-side bridge.

### How It Works

The owning Process Component is authoritative for a Process-backed Skill's behavior, responsibility, inputs, outputs, authority, verification, and stopping conditions. Agent Skill Preferences bridge that Component to Agent Sync; the selected Runtime owns execution mechanics. An external provider can supply a different realization, but it does not change the owning Component's meaning.




<br><br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Skill** — a reusable capability activated explicitly or by a declared coordinator.
- **Skill Preferences** — the Agent-side bridge to one Skill's owning Component, including its invocation and Runtime boundary.
- **Capability Realization Kind** — the declared way a Skill becomes usable: Constructed from its Process Component and Agent Skill Preferences, or Installed through a provider.




<br><br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Agent, Implementation, and Target** — reads the authorities required by its Agent Skill Preferences and owning Process Component.
- **Consumed by Agent and permitted Coordinators** — provides an executable capability without acquiring the authority of its sources.
- **Realized by Agent Sync** — is carried into the selected Runtime without changing its owning Component.




<br><br>

<!--------------------------------------------------------------------------------- Shared Guidance --->
## Shared Guidance

### Each Skill layer has one owner

**Rule:** This Definition explains the shared Skill concept, the owning Process Component owns Process-specific behavior, Agent Skill Preferences provide the bridge, and the selected Runtime owns execution mechanics.

**Why:** Clear ownership prevents duplication and conflicting authorities.

**Boundary:** No layer replaces, overrides, or duplicates another layer's authority.


### Every Skill has one owner and bridge

**Rule:** Every Process-backed Skill has one owning Process Component and one Agent Preferences bridge that points to it.

**Why:** One owning Component keeps each Process Skill's behavior clear and consistent, while one Preferences bridge keeps the Agent mapping clear.

**Boundary:** Agent Skill Preferences do not repeat or redefine the owning Process Component's workflow.


### Skill availability is proven

**Rule:** A Skill is usable only when the selected Runtime can discover and invoke it.

**Why:** A declaration alone does not make a capability available.

**Boundary:** Invocation never expands the Skill's authority or responsibility.


### Skill execution is repeatable

**Rule:** Repeating a Skill preserves valid work and avoids unnecessary changes.

**Why:** Skills may be resumed or invoked more than once.

**Boundary:** Repeatability never authorizes destructive replacement of meaningful work.


### Every Skill has one Realization Kind

**Rule:** Each Skill has one realization path: Constructed or Installed.

**Why:** The Runtime needs one clear realization path for every Skill.

**Boundary:** Realization never changes the Contract's meaning or authority.


### Skill owns executable capability only

**Rule:** A Skill owns its executable capability and does not own Target meaning, Implementation policy, Runtime mechanics, or another Component's records.

**Why:** Clear ownership keeps reusable capability separate from the authorities it consumes.

**Boundary:** A Skill may read required authorities and produce its declared outputs without acquiring ownership of them.




<br><br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

**Each Skill layer has one owner** — Definition explains the shared concept; Process Component owns Skill behavior; Preferences bridge Agent to Process; Runtime owns execution mechanics.

**Every Skill has one owner and bridge** — define each Process-backed Skill through one owning Component and one Agent Preferences bridge.

**Skill availability is proven** — verify Runtime discovery and invocation; never infer availability from declaration alone.

**Skill execution is repeatable** — preserve valid work on repetition; never replace meaningful work destructively.

**Every Skill has one Realization Kind** — use exactly one of Constructed or Installed.

**Skill owns executable capability only** — keep ownership limited to the declared capability.

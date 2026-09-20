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
4. **[Principles](#principles)**
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

Skill prevents the Agent from having to reconstruct the same instructions each time. Each Skill has one clear responsibility and one authoritative Contract.

### How It Works

The Skill Contract defines the Skill's behavior. Preferences hold its current selections and declarations. The Capability Realization Kind determines how the Skill becomes usable. Agent Sync carries the Skill into the selected Runtime; the Runtime owns its execution mechanics.





<br><br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Skill** — a reusable capability activated explicitly or by relevance.
- **Skill Contract** — the authoritative definition of one Skill's behavior, responsibility, inputs, outputs, and boundaries.
- **Capability Realization Kind** — the declared way a Skill becomes usable in a Runtime.





<br><br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Agent, Implementation, and Target** — reads the authorities required by its responsibility.
- **Consumed by Agent and permitted Coordinators** — provides an executable capability.
- **Realized by Agent Sync** — is carried into the selected Runtime without changing its authority.





<br><br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

### Each Skill layer has one owner

**Rule:** Definition owns shared Principles, Contract owns Skill-specific behavior, Preferences own current declarations, and the selected Runtime owns execution mechanics.

**Why:** Clear ownership prevents duplication and conflicting authorities.

**Boundary:** No layer replaces, overrides, or duplicates the authority of another layer.


### Every Skill has one Contract

**Rule:** Every declared Skill has one complete Contract that defines its responsibility, behavior, inputs, outputs, authority, verification, and stopping conditions.

**Why:** One Contract keeps each Skill's behavior clear and consistent.

**Boundary:** This Definition does not repeat a Skill Contract or define one Skill's workflow.


### Skill availability is proven

**Rule:** A Skill is usable only when the selected Runtime can discover and invoke it.

**Why:** A declaration alone does not make a capability available.

**Boundary:** Invocation never expands the Skill's authority or responsibility.


### Skill execution is repeatable

**Rule:** Repeating a Skill preserves valid work and avoids unnecessary changes.

**Why:** Skills may be resumed or invoked more than once.

**Boundary:** Repeatability never authorizes destructive replacement of meaningful work.


### Every Skill has one Realization Kind

**Rule:** Each Skill declares one Capability Realization Kind that determines how it becomes usable.

**Why:** The Runtime needs one clear realization path for every Skill.

**Boundary:** Realization never changes the Skill Contract's meaning or authority.


### Skill owns executable capability only

**Rule:** A Skill owns its executable capability and does not own Target meaning, Implementation policy, Runtime mechanics, or another Component's records.

**Why:** Clear ownership keeps reusable capability separate from the authorities it consumes.

**Boundary:** A Skill may read required authorities and produce its declared outputs without acquiring ownership of them.





<br><br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

**Each Skill layer has one owner**

- **Must** — keep Principles, Contract behavior, Preferences, and Runtime mechanics in their owning layers.
- **Never** — duplicate or override another layer's authority.

**Every Skill has one Contract**

- **Must** — define each Skill through one authoritative Contract.
- **Never** — duplicate Skill-specific workflow in this Definition.

**Skill availability is proven**

- **Must** — verify that the selected Runtime can discover and invoke the Skill.
- **Never** — infer availability from a declaration alone.

**Skill execution is repeatable**

- **Must** — preserve valid work on repetition.
- **Never** — use repeatability to justify destructive replacement.

**Every Skill has one Realization Kind**

- **Must** — give each Skill one realization path.
- **Never** — let realization alter the Contract.

**Skill owns executable capability only**

- **Must** — keep ownership limited to the declared capability.
- **Never** — let a Skill acquire another Component's authority.

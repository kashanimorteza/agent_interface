# Implement Definition

Implement is the Operation Component that coordinates the authorized Operations sequence across the selected phases.

Responsibility: Coordination of the Operations workflow across configuration, planning, development, and review.

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

Implement is the Operation Component that coordinates Configure, Plan, Develop, and Review across the selected phases under the current authorities.

### Purpose

Implementation work needs one accountable workflow that can move through planning, development, and review without allowing one operation to silently replace another.

### How It Works

Implement reads the selected phase or phases, ensures the Config records are ready, and invokes the applicable primary Operations in order. It carries forward their outcomes and stops when a required condition or human decision prevents safe continuation.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Implementation Cycle** — one coordinated passage through the applicable Operations for a selected phase.
- **Operation Outcome** — the recorded result of one coordinated Operation.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes State and Plan** — determines the current position and work to coordinate.
- **Consumes Development and Target** — carries their authorities into the workflow.
- **Consumed by State** — supplies aggregate outcomes and stopping information.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Implement owns coordination, not the work performed by Configure, Plan, Develop, Review, or State. Each participating Component retains its own authority and records.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principle and Operation Contract in this Definition govern coordination. Implement Preferences supply only coordination defaults and never replace an owning Component's authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Implement coordinates the Operations workflow

**Rule:** Implement is the only primary Operation that invokes another primary Operation Skill. It coordinates Configure, Plan, Develop, and Review in the authorized sequence, preserving each Component's scope, authority, outcomes, and stopping conditions.

**Why:** One coordinator keeps the implementation cycle coherent without turning coordination into ownership of the work it invokes.

**Boundary:** Implement never changes a Plan, Development result, Review Finding, or State record outside the authority of its owning Component.

<br>

<!--------------------------------------------------------------------------------- Operation Contract --->
## Operation Contract

Implement is the coordinating Operation for zero or more phase selections. An empty selection means every phase currently enabled and ready. It resolves and validates the complete selection before mutation and preserves Target order.

Implement does not establish an independent Interface or Target Understanding. It invokes Configure, Plan, Develop, and Review, and each invoked Skill establishes the Understanding required for its own work. It never enters the Agent Module to resolve them.

Implement checks whether the three Config records are ready and invokes Configure when they are missing or structurally unready. For each selected phase it runs Plan, then Develop, then Review. When no phase is selected, it applies this sequence to every enabled phase. Review owns its internal recheck cycle; Implement does not invoke Plan or Develop on Review's behalf.

Implement owns only its own coordination Log Entry. Every delegated mutation remains owned by the invoked Operation Component, and every child Operation writes its own State Log Entry. It never bypasses Human approval, combines operation ownership, invokes Reset or Agent Native, or changes Target intent.

Implement stops on invalid input, unavailable or incompatible child Skill, unmet dependency, failed operation gate, an unresolved Review blocker, or a required Human decision.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Implement coordinates the Operations workflow**

- **Must** — preserve the declared sequence and authority of Configure, Plan, Develop, and Review.
- **Never** — take ownership of another Operation Component's records or results.

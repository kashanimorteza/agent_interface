# Implement Definition

Implement is the Operation Component that coordinates the authorized Operations sequence across the selected phases.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Layering](#layering)**
5. **[Authority](#authority)**
6. **[Principles](#principles)**
7. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Implement is the Operation Component that coordinates Configure, Plan, Develop, and Review across the selected phases.

### Purpose

Implementation work needs one accountable workflow that can move through planning, development, and review without allowing one operation to silently replace another.

### How It Works

Implement accepts one or more selected phases, or coordinates every phase when none is selected. For each selected phase, it first ensures the required Config records are available, coordinating Configure when they are not. It then coordinates Plan, Develop, and Review in that order, carrying each outcome forward and stopping when a required condition or unresolved decision prevents safe continuation. Every execution appends one Implement Log Entry to State, recording common execution fields and coordination-specific outcomes in its `data`. Implement does not establish Target or Interface Understanding for the work; each participating Operation establishes the Understanding required for its own responsibility.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Implementation Cycle** — one coordinated passage through the applicable Operations for a selected phase.
- **Operation Outcome** — the recorded result of one coordinated Operation.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Coordinates Configure, Plan, Develop, and Review** — invokes each Operation in the required order while each retains responsibility for its own Understanding, work, and outcome.
- **Records in State** — appends its coordination outcome and stopping information to its own Log Entry.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Implement owns coordination, not the work performed by Configure, Plan, Develop, Review, or State. Each participating Component retains its own authority and records.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principle in this Definition governs coordination. Implement Preferences supply only coordination defaults and never replace an owning Component's authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Implement coordinates the Operations workflow

**Rule:** Implement coordinates the selected phases, or every phase when none is selected. For each phase, it ensures required Config records are available, then coordinates Plan, Develop, and Review in that order, preserving each Component's scope, authority, outcomes, and stopping conditions. It records its coordination outcome in an Implement Log Entry.

**Why:** One coordinator keeps the implementation cycle coherent without turning coordination into ownership of the work it coordinates.

**Boundary:** Apart from appending its own Implement Log Entry, Implement never changes a Plan, Development result, Review Finding, or State record outside the authority of its owning Component.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Implement coordinates the Operations workflow**

- **Must** — coordinate the selected phases, or every phase when none is selected, ensure Config is available before coordinating Plan, Develop, and Review in that order, and record its coordination outcome in its Log Entry.
- **Never** — take ownership of another Operation Component's records or results.

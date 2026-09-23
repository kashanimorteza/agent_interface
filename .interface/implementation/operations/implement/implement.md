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

Implement accepts one or more Target phase identifiers, or coordinates every Target phase in Target order when none is selected. It reserves its Implement Log identifier, then checks the required Config records once and coordinates Configure only when they are absent or invalid. Once Config is available, it records the active Workflow position as `implementing` and writes its Implement Log Entry with that reserved identifier. It then coordinates Plan, Develop, and Review for each phase in that order. A blocked Develop does not by itself skip Review: when Source is available, Review still examines it and records its outcome. Review continues its own passes until its result is satisfied or a Blocker prevents continuation. Each coordinated Operation Log Entry records the reserved Implement Log identifier as its `parent_id`. Implement carries outcomes forward; unresolved Blockers or Open Questions may make its final outcome blocked, but do not prevent an applicable Review. Its Log records common execution fields, coordination-specific outcomes, and the unique counts of associated Open Questions and Blockers in `data`. Implement does not establish Target or Interface Understanding for the work; each participating Operation establishes the Understanding required for its own responsibility.

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

**Rule:** Implement accepts one or more Target phase identifiers, or coordinates every Target phase in Target order when none is selected. It reserves its Implement Log identifier, then checks required Config records once and coordinates Configure only when they are absent or invalid. Once Config is available, it records the active Workflow position as `implementing` and writes its Implement Log Entry with that reserved identifier. For each phase, it coordinates Plan, Develop, and Review in that order. A blocked Develop does not by itself skip Review: when Source is available, Review performs its own passes until its result is satisfied or a Blocker prevents continuation. Every coordinated Operation Log Entry records the reserved Implement Log identifier as its `parent_id`. Implement preserves each Component's scope and outcome, records its coordination outcome, and records the unique counts of associated Open Questions and Blockers in its Log Entry's `data`.

**Why:** One coordinator keeps the implementation cycle coherent without turning coordination into ownership of the work it coordinates.

**Boundary:** Apart from appending its own Implement Log Entry, Implement never changes a Plan, Development result, Review Finding, or State record outside the authority of its owning Component.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Implement coordinates the Operations workflow**

- **Must** — accept one or more Target phase identifiers, or every Target phase in Target order when none is selected.
- **Must** — reserve its Log identifier, check Config once, coordinate Configure only when Config is absent or invalid, then record `implementing` and its Log Entry.
- **Must** — coordinate Plan, Develop, and Review in that order for each phase; a blocked Develop does not skip an applicable Review.
- **Must** — record the Implement Log Entry as `parent_id` in every coordinated Operation Log Entry, coordination outcomes, and unique Open Question and Blocker counts in its own Log Entry.
- **Never** — take ownership of another Operation Component's records or results.

# Implement Definition

Implement is the Operation Component that coordinates the authorized Operations sequence across the selected phases.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Authority](#authority)**
6. **[Principles](#principles)**
7. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Implement is the single entry point that runs the full Operations workflow for one or more phases.

### Purpose

Implementation work needs one accountable workflow that can move through planning, development, and review without allowing one operation to silently replace another.

### How It Works

Implement runs the Operations for each selected phase in order, starting Configure only when the Config records need it, and carries each Operation's outcome into its own aggregate result.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Operation Outcome** — the recorded result of one coordinated Operation.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

Implement owns coordination, not the work performed by Configure, Plan, Develop, Review, or State. Each participating Component retains its own authority and records.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Configure, Plan, Develop, and Review** — invokes each in order; each keeps its own work and outcome.

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

**Rule:** Implement accepts one or more Target phase identifiers, or coordinates every Target phase in Target order when none is selected. It checks required Config records once and coordinates Configure only when they are absent or invalid. If Config remains absent or invalid after that attempt, Implement stops before Plan, Develop, or Review. Otherwise, for each phase, it coordinates Plan, Develop, and Review in that order. A blocked Develop does not by itself skip Review: when Source is available, Review performs its own passes until its result is satisfied or a Blocker prevents continuation. Implement preserves each Component's scope and outcome and determines the aggregate counts of associated Open Questions and Blockers; unresolved Blockers or Open Questions may make its final outcome blocked, but never prevent an applicable Review. Implement does not establish Target or Interface Understanding; each participating Operation establishes the Understanding its own responsibility requires.

**Why:** One coordinator keeps the required Operations sequence coherent without turning coordination into ownership of the work it coordinates.

**Boundary:** Implement never changes a Plan, Development result, Review Finding, or State record outside the authority of its owning Component.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Implement coordinates the Operations workflow**

- **Must** — accept one or more Target phase identifiers, or every Target phase in Target order when none is selected.
- **Must** — check Config once and coordinate Configure only when Config is absent or invalid.
- **Must** — stop before Plan, Develop, and Review if required Config remains absent or invalid after Configure.
- **Must** — coordinate Plan, Develop, and Review in that order for each phase; a blocked Develop does not skip an applicable Review.
- **Never** — take ownership of another Operation Component's records or results.

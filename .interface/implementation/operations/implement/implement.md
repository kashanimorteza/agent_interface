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
7. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Implement is the Operation Component that coordinates Configure, Plan, Develop, and Review across the selected phases under the current authorities.

### Purpose

Implementation work needs one accountable workflow that can move through planning, development, and review without allowing one operation to silently replace another.

### How It Works

Implement coordinates the applicable work in order, carries forward its outcomes, and stops when a required condition or unresolved decision prevents safe continuation.

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

The Principle in this Definition governs coordination. Implement Preferences supply only coordination defaults and never replace an owning Component's authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Implement coordinates the Operations workflow

**Rule:** Implement coordinates Configure, Plan, Develop, and Review in the authorized sequence, preserving each Component's scope, authority, outcomes, and stopping conditions.

**Why:** One coordinator keeps the implementation cycle coherent without turning coordination into ownership of the work it coordinates.

**Boundary:** Implement never changes a Plan, Development result, Review Finding, or State record outside the authority of its owning Component.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Implement coordinates the Operations workflow**

- **Must** — preserve the declared sequence and authority of Configure, Plan, Develop, and Review.
- **Never** — take ownership of another Operation Component's records or results.

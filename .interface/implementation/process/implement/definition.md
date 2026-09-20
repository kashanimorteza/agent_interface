# Implement Definition

<br><br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[Implement coordinates the Process workflow](#implement-coordinates-the-process-workflow)**
5. **[At a Glance](#at-a-glance)**

<br><br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Implement is the Process Component that coordinates the workflow across Plan, Develop, and Review under the current authorities.

### Purpose

Implementation work needs one accountable workflow that can move through planning, development, and review without allowing one operation to silently replace another.

### How It Works

Implement reads State and the selected authorities, invokes the applicable Process operations in order, carries forward their outcomes, and stops when a required condition or human decision prevents safe continuation.

<br><br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Implementation Cycle** — one coordinated passage through the applicable Process operations for a selected phase.
- **Process Outcome** — the recorded result of one coordinated Process operation.

<br><br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes State and Plan** — determines the current position and work to coordinate.
- **Consumes Development and Target** — carries their authorities into the workflow.
- **Consumed by State** — supplies aggregate outcomes and stopping information.

<br>

Implement owns coordination, not product Source, Plan content, Review Findings, or State authority.

Every Principle in this file is mandatory. A Process Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br><br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Implement coordinates the Process workflow

**Rule:** Implement coordinates only the authorized sequence of Plan, Develop, and Review operations, preserving each Component's scope, authority, outcomes, and stopping conditions.

**Why:** One coordinator keeps the implementation cycle coherent without turning coordination into ownership of the work it invokes.

**Boundary:** Implement never changes a Plan, Development result, Review Finding, or State record outside the authority of its owning Component.

<br><br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Implement coordinates the Process workflow**

- **Must** — preserve the declared sequence and authority of Plan, Develop, and Review.
- **Never** — take ownership of another Process Component's records or results.

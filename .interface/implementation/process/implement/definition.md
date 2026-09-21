# Implement Definition

Implement is the Process Component that coordinates the authorized Process sequence across the selected phases.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Layering](#layering)**
5. **[Authority](#authority)**
6. **[Principles](#principles)**
7. **[Process Contract](#process-contract)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Implement is the Process Component that coordinates the workflow across Plan, Develop, and Review under the current authorities.

### Purpose

Implementation work needs one accountable workflow that can move through planning, development, and review without allowing one operation to silently replace another.

### How It Works

Implement reads State and the selected authorities, invokes the applicable Process operations in order, carries forward their outcomes, and stops when a required condition or human decision prevents safe continuation.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Implementation Cycle** — one coordinated passage through the applicable Process operations for a selected phase.
- **Process Outcome** — the recorded result of one coordinated Process operation.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes State and Plan** — determines the current position and work to coordinate.
- **Consumes Development and Target** — carries their authorities into the workflow.
- **Consumed by State** — supplies aggregate outcomes and stopping information.

<br>

Implement owns coordination, not product Source, Plan content, Review Findings, or State authority.

Every Principle in this file is mandatory. A Process Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Implement owns coordination, not the work performed by Configure, Plan, Develop, Review, Launch, Reset, or State. Each participating Component retains its own authority and records.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principle and Process Contract in this Definition govern coordination. Implement Preferences supply only coordination defaults and never replace an owning Component's authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Implement coordinates the Process workflow

**Rule:** Implement coordinates only the authorized sequence of Plan, Develop, and Review operations, preserving each Component's scope, authority, outcomes, and stopping conditions.

**Why:** One coordinator keeps the implementation cycle coherent without turning coordination into ownership of the work it invokes.

**Boundary:** Implement never changes a Plan, Development result, Review Finding, or State record outside the authority of its owning Component.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
<!--------------------------------------------------------------------------------- Process Contract --->
## Process Contract

Implement is the explicit Human coordinator for zero or more phase selections. An empty selection means every phase currently enabled and ready. It resolves and validates the complete selection before mutation and preserves Target order.

Implement establishes current Interface and Target Understanding, resolves the synchronized Runtime implementations of Configure, Plan, Develop, Review, and Launch, and proves that each is available for coordinator invocation. It never enters the Agent Module to resolve them.

When no phase is selected, Implement runs Configure exactly once and verifies readiness. For each phase it runs the required Plan → Develop → Review cycle, reconciles Findings through their owning operations, and repeats only while the cycle closes or materially advances a Finding. It advances only after current Plan and Implementation Assurance succeed.

Implement owns only its own status and step-by-step run log. Every delegated mutation remains owned by the invoked Process Component. It never bypasses Human approval, combines operation ownership, invokes Reset or Agent Native, or changes Target intent.

Launch is eligible only after every enabled and ready phase has completed Planning and Development and has satisfied the required Review assurances. Implement stops on invalid input, unavailable or incompatible child Skill, unmet dependency, failed operation gate, repeated unresolved Finding, no observable progress, inconclusive assurance, or required Human decision.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Implement coordinates the Process workflow**

- **Must** — preserve the declared sequence and authority of Plan, Develop, and Review.
- **Never** — take ownership of another Process Component's records or results.

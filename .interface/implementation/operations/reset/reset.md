# Reset Definition

Reset is the Operation Component that reconciles authorized operational records and outputs with a selected reset scope.

Responsibility: The bounded reconciliation of operational records and outputs after an authorized reset.

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

Reset is the Operation Component that reconciles operational records and implementation outputs with an explicitly authorized reset scope while preserving what must remain.

### Purpose

Long-running implementation work needs a safe way to remove or reconcile selected outputs without erasing unrelated progress, evidence, or human-owned intent.

### How It Works

Reset reads the selected scope and current authorities, identifies affected records and outputs, preserves protected content, performs only the authorized reconciliation, and records the resulting position.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Reset Scope** — the explicit set of records or outputs a Reset operation may reconcile.
- **Protected Content** — content outside the authorized scope or owned by a different authority that Reset must preserve.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes State and Config** — identifies the current operational position and records to reconcile.
- **Consumes the selected authorities** — determines what may be reset and what must remain.
- **Consumed by State** — supplies the resulting operational position and history.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Reset owns reconciliation of its authorized scope. It does not redefine Target, repair product implementation, or take ownership of another Operation Component's records.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principle and Operation Contract in this Definition govern Reset. Reset Preferences can guide only an explicitly authorized scope and cannot authorize a destructive scope themselves.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Reset reconciles only its authorized scope

**Rule:** Reset changes only the records and outputs explicitly included in its authorized scope, preserves protected content and meaningful history, and records what it removed or retained.

**Why:** A reset must make the selected state recoverable without turning cleanup into silent destruction of unrelated work.

**Boundary:** Reset never changes Target intent, Principles, Preferences, or Development results outside its explicit scope.

<br>

<!--------------------------------------------------------------------------------- Operation Contract --->
## Operation Contract

Reset accepts exactly one scope: explicit phases, all phases with generated work, `config`, or `complete`. It resolves phase identity, ownership, generated outputs, State, Plan, Review, Config, Platform Launch authorities, Task evidence, and observable repository state before mutation.

Reset always produces a complete preview and requires explicit Human confirmation. It removes or resets only exact targets in the confirmed scope, preserves Interface and Target sources, protected content, unselected phases, and meaningful surviving history, and records the resulting State.

An explicit-phase reset removes that phase's Plan, Task content and history, Review and Findings, attributable implementation output, and aggregate progress. Argument-free reset applies the same behavior to every discovered phase with generated work. Config reset removes operational Config files without regenerating them. Complete reset combines Config reset with all-phase reset while preserving the Config container and Environment preparation.

Reset resolves shared paths conservatively; unresolved attribution stops mutation. It stops affected runtime parts in dependency order, uses bounded file removal, verifies every previewed target and every protected target, and never invokes another workflow operation. Repeating an already realized reset produces no additional deletion beyond a newly resolved and confirmed preview.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Reset reconciles only its authorized scope**

- **Must** — preserve protected content and record the reset outcome.
- **Never** — alter anything outside the authorized reset scope.

# Reset Definition

Reset is the Operation Component that reconciles authorized operational records and outputs with a selected reset scope.


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

Reset preserves everything outside that scope.

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

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Reset owns reconciliation of its authorized scope. It does not redefine Target, repair product implementation, or take ownership of another Operation Component's records.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principles in this Definition govern Reset. Reset Preferences can guide only an explicitly authorized scope and cannot authorize a destructive scope themselves.

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

### Reset previews and confirms before it removes

**Rule:** Reset accepts exactly one scope: explicit phases, all phases with generated work, `config`, or `complete`. Before mutation it resolves phase identity, ownership, generated outputs, State, Plan, Review, Config, Platform Launch authorities, Task evidence, and observable repository state, produces a complete preview, and requires explicit Human confirmation. An explicit-phase reset removes that phase's Plan, Task content and history, Review and Findings, attributable implementation output, and aggregate progress; an argument-free reset applies the same to every phase with generated work. A Config reset removes the operational Config files without regenerating them, and a complete reset combines Config reset with all-phase reset while preserving the Config container and Environment preparation. Reset removes or resets only exact targets in the confirmed scope, preserves Interface and Target sources, protected content, unselected phases, and meaningful surviving history, stops affected runtime parts in dependency order, uses bounded file removal, verifies every previewed and every protected target, and records the resulting State.

**Why:** Removal is irreversible, so the Human sees and confirms exactly what will be removed before anything is.

**Boundary:** Reset resolves shared paths conservatively and refuses an ambiguous or unsafe reset; unresolved attribution stops mutation. Repeating an already realized reset removes nothing beyond a newly resolved and confirmed preview.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Reset reconciles only its authorized scope**

- **Must** — preserve protected content and record the reset outcome.
- **Never** — alter anything outside the authorized reset scope.

**Reset previews and confirms before it removes**

- **Must** — preview the complete scope and obtain explicit Human confirmation before any removal.
- **Never** — remove a target whose attribution is unresolved.

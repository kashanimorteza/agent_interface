---
name: my-interface-configure
description: Core Interface Skill for configuring. Creates or reconciles the Config records declared by Configure Preferences under .interface/config/ from their current Schemas, records the Workflow position `configuring`, and appends one Configure Log Entry to State. Use when Config records are missing or invalid, before Plan, Develop, or Review, or when the Human asks to configure the Interface.
---

<!--
Native realization (Claude Code) of the Core Skill Contract `configure`, synchronized by
/my-interface-agent-native. The Human-owned Agent Module remains authoritative; this Skill is
not a second authority. Its operational meaning is owned by the Configure Operation Component,
which this Skill reads from its current location at run time.
-->

# Configure (`my-interface-configure`)

Stable key: `configure`. Required. Invocable directly by the Human (`/my-interface-configure`) or by an Agent.

- **Input:** an invocation request.
- **Output:** the Skill execution result and status.

## Before acting

1. Apply the synchronized project Rules (`.claude/rules/`), especially *Agent Interface Skill policy* and *Agent Interface bootstrap*. They are this Skill's Agent-side contract.
2. Establish Interface Understanding from `.interface/interface.md` and the Foundation section files it links.
3. Through the Interface, locate and read the Configure Operation Component: its Definition (currently `.interface/implementation/operations/configure/configure.md`) and Preferences (`configure.yaml`). They own this Skill's meaning, Principles, the Config directory, and the record-to-Schema mappings. When they differ from the summary below, they win.

## What Configure does

- Reads **only** the Config Schemas declared by Configure Preferences.
- Generates each declared Config Record from its current Schema, preserving the explanatory comments the Schema defines.
- When a record already exists, preserves its valid operational content and changes only what is required to restore Schema conformance.
- Once the State Config is available, records the active Workflow position as `configuring` and appends **one** Configure Log Entry to the State record: common execution fields in the entry, Configure-specific details in its `data`. Establish the Log Entry shape from the State Config's Schema.
- Is complete when every generated record conforms to its current Schema.

## Stop conditions

Stop and report the exact reason when a required Schema or mapping is invalid or unavailable, or when an authorized Config record or Log Entry cannot be written.

## Write authority (fixed at invocation)

- Only the three Config Records declared by Configure Preferences, inside `.interface/config/`, and Configure's own Log Entry / Workflow position in State.
- Never perform another Operation (Plan, Develop, Review, Implement) and never change anything outside those records. Later operational content belongs to the Operation that owns it.
- Every other `.interface/` path is read-only (enforced by the project's PreToolUse guard).

## Report

State which records were created, reconciled, or already conformant; the Log Entry written; the Skills actually used; and any stop reason, using the capability status vocabulary from the Skill policy Rule where capability health is involved.

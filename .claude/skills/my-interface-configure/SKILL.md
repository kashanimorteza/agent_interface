---
name: my-interface-configure
description: Core Interface Skill "Configure" (stable key `configure`). Creates or reconciles the structural Config records (Application, Plan, State) in the Interface Config directory from their current Schemas, records the Workflow position `configuring`, and appends one Configure Log Entry to State. Use when the Interface Config records are missing, invalid, or must be reconciled, or when another Core Skill reports that Configure is required.
---

# Configure

The Core Skill for configuring. Required. Stable key: `configure`. Skill name: `my-interface-configure`.

This Skill is a synchronized Runtime realization. It never reads, searches, or resolves the Agent Module; a missing or unusable Runtime capability is reported as Runtime drift and the Human is asked to run Agent Native Sync.

## Contract

- **Inputs:** an invocation request.
- **Invocation:** may be invoked directly by a Human (`/my-interface-configure`) or by an Agent (Skill tool).
- **Outputs:** the Skill execution result and status.

## Start of workflow

1. Apply the Runtime Rules `interface-bootstrap` and `interface-skill-policy` (`.claude/rules/`) before anything else.
2. Establish Interface Understanding from `.interface/interface.md` and the Foundation section files it links.
3. Locate through the Interface, then read completely, the current **Configure Operation Component** Definition and Preferences (currently `.interface/implementation/operations/configure/configure.md` and `configure.yaml`). They are the authority for this Skill's meaning; this file only summarizes them, and on any difference the current Operation sources win.

## What Configure does

- Reads **only** the Config Schemas declared by Configure Preferences and generates or reconciles **only** the corresponding Config Records in the declared Config directory.
- Preserves every explanatory comment defined by each Schema in the generated record.
- When a record already exists, preserves its valid operational content and changes only what is required to restore Schema conformance.
- Once the State Config is available, records the active Workflow position as `configuring` and appends exactly one Configure Log Entry to State (common execution fields in the entry, Configure-specific details in its `data`), following the State rules and State Schema located through the Interface.
- Complete when every generated record conforms to its current Schema.

## Stop when

- a required Schema or mapping is invalid or unavailable; or
- an authorized Config record or Log Entry cannot be written.

Always report the reason for stopping.

## Never

- perform another Operation, or interpret project meaning;
- change anything outside the declared Config Records and its own Configure Log Entry (the rest of `.interface/` stays read-only);
- write operational content owned by a later Operation.

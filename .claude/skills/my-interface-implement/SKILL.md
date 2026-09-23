---
name: my-interface-implement
description: Core Interface Skill "Implement" (stable key `implement`). Coordinates the Operations workflow across the selected (or every) Target phase - Configure only when Config is absent or invalid, then Plan, Develop, and Review per phase in that order - recording its own Implement Log Entry as the parent of every coordinated Log Entry. Use to run the full implementation cycle. Optional argument - one or more Target phase identifiers.
argument-hint: "[phase-id ...]"
---

# Implement

The Core Skill for implementing. Required. Stable key: `implement`. Skill name: `my-interface-implement`.

This Skill is a synchronized Runtime realization. It never reads, searches, or resolves the Agent Module; a missing or unusable Runtime capability is reported as Runtime drift and the Human is asked to run Agent Native Sync.

## Contract

- **Inputs:** an invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers).
- **Invocation:** may be invoked directly by a Human (`/my-interface-implement`) or by an Agent (Skill tool).
- **Outputs:** the Skill execution result and status.

## Start of workflow

1. Apply the Runtime Rules `interface-bootstrap` and `interface-skill-policy` (`.claude/rules/`) before anything else.
2. Locate through the Interface, then read completely, the current **Implement Operation Component** Definition and Preferences (currently `.interface/implementation/operations/implement/implement.md` and `implement.yaml`). They are the authority; this file only summarizes them, and on any difference the current sources win.

Implement does not establish Target or Interface Understanding for the work itself; each coordinated Skill establishes the Understanding its own responsibility requires.

## Coordinated Skills

| Operation | Runtime Skill |
|---|---|
| Configure | `my-interface-configure` |
| Plan | `my-interface-plan` |
| Develop | `my-interface-develop` |
| Review | `my-interface-review` |

Invoke each through the Skill tool, passing the phase identifier(s) where the Skill accepts them.

## Procedure

1. **Phases.** Use the selected phase identifiers, or every Target phase in Target order when none is selected.
2. **Reserve** the Implement Log identifier (following the State rules located through the Interface).
3. **Check the required Config records once.** Coordinate `my-interface-configure` only when they are absent or invalid.
4. Once Config is available, record the active Workflow position as `implementing` and write the Implement Log Entry with the reserved identifier.
5. For each phase, in order: coordinate `my-interface-plan`, then `my-interface-develop`, then `my-interface-review`. Review runs its own passes until its result is satisfied or a Blocker prevents continuation.
6. Every coordinated Operation Log Entry records the reserved Implement Log identifier as its `parent_id` — pass it to each coordinated Skill.
7. Carry each Operation Outcome forward; record coordination-specific outcomes and stopping information in the Implement Log Entry's `data`.

## Stop when

A required condition, Blocker, or unresolved decision prevents safe continuation. Always report the reason and which Operation stopped.

## Never

Apart from appending its own Implement Log Entry, change a Plan, Development result, Review Finding, or State record outside the authority of its owning Component, or take ownership of another Operation's records or results.

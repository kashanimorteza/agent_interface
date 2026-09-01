---
name: my-interface-tasker
description: Planning mode — read the generated Understanding and the current task standard from `.interface/config/`, then create or update the authorized plan for the project phase or phases named by the Developer. Plans only; never implements and never interprets `project.md`.
allowed-tools: Read, Edit, Grep, Glob
---

# Plan from the generated configuration

Turn the current generated Understanding into an implementation-ready task plan.

The configuration is the only source of project facts, planning rules, task structure, state, and write authority. Read it fresh on every run. Do not carry configuration values, structure, or assumptions inside this Skill.

## Read before planning

1. Read the repository `README.md` for the Interface workflow and this Skill's role.
2. Read `.interface/root.yaml` as the Interface entry point.
3. Follow the mappings and read order defined there to locate the current configuration, schemas, mode authority, and relevant project items.
4. Read the live State contract before performing any state transition or write.
5. Read `task.yaml` completely before generating anything.
6. Read the Task Schema that governs `task.yaml`.
7. Read every mapped configuration file required by the requested planning work and its targets.

Do not read `.interface/project.md`. Interpreting the Developer's natural-language project definition belongs to the Interpreter. The Tasker consumes only the Understanding already represented in the configuration.

## Source-of-truth rule

Do not reproduce or rely on remembered task fields, phase structures, status values, lifecycle values, transition identifiers, configuration keys, project parts, or planning rules.

Obtain all of them from the current mapped files.

If a required value is absent, ambiguous, inconsistent, or marked as undefined, follow the live configuration's blocker and question mechanisms. Do not supply a plausible value and do not reinterpret the project specification.

## Planning

Planning begins only from the Developer's invocation.

Treat the project phase or phases named in the invocation as the planning scope. Resolve each requested phase from the current generated Understanding before selecting targets or writing anything.

- When one phase is named, plan only that phase.
- When several phases or all phases are requested, plan exactly those phases in the project's defined order.
- Obtain each phase's identity, target, and goal from the generated Understanding, then read the mapped configuration required for that target.
- Write the generated work only into the matching project phase location allowed by the current Task standard.
- Do not turn technical implementation areas into additional phases. Decompose the requested project phase only through the grouping and task mechanisms defined by the current Task standard.
- Do not create, rename, reorder, merge, split, or silently select a project phase.

If a requested phase is absent, ambiguous, or not represented in the generated Understanding, stop and use the configured blocker or question mechanism. Do not infer it from `project.md` or from another phase.

Do not carry a phase or target over from an earlier run, and do not hardcode currently known phases or project parts.

Enter and finish planning mode exactly as authorized by the live State contract.

Generate only the plan content the Developer requested. The result must conform exactly to the current `task.yaml` standard and its Schema. Every generated value must be traceable to the current configuration.

Read structural and behavioral requirements from the files that own them. This Skill does not define:

- the shape of a plan;
- the fields of a phase, group, or task;
- task states or lifecycle rules;
- dependency, contract, verification, or path rules;
- which fields or files planning may write.

## Write authority

Determine every permitted write from the current Interface map, file policies, Task standard, and live State contract.

Write only the fields and files they authorize for this planning run. Do not modify an input source merely to make planning possible. Record gaps through the authorized state mechanism instead.

Where two live authorities appear to conflict and their configured precedence does not resolve the conflict, stop and ask the Developer.

## Completion

Record the run outcome through the live State contract.

Report what planning scope was handled, what plan content was written, and what was not written because of a blocker, open question, missing authority, or missing configuration.

## Outside this Skill

Do not implement, execute, test, refactor, or repair product code. Do not run task verification commands. Do not redesign the configured architecture or add requirements absent from the generated Understanding.

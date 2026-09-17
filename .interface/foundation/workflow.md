# Workflow

This file carries the Workflow section of the Interface, moved here verbatim from `interface.md` on 2026-09-17. It is part of Interface Understanding: every Skill reads `interface.md` and this file before acting. The Interface file remains the canonical entry point; this file is one of its sections.

<br><br>

## Define the Project

Define the Target before selecting a Workflow Path:

```text
Human Definition = .interface/target/non-technical.md
Technical Definition = .interface/target/technical.md
```

The Human states the intended outcome in Human Definition, then records its corresponding technical definition without changing that intent.

After the Project is defined, select Default, Normal, or Detailed. The path controls only how much of the Workflow the Human invokes directly; it does not change any operation contract or verification gate.



<br><br>

## Default

For the simplest complete run:

```text
/my-interface-implement
```

Implement processes all enabled and ready phases and performs Launch when every required gate is satisfied.



<br><br>

## Normal

For complete orchestration with phase selection:

Run phases separately:

```text
/my-interface-implement 1
/my-interface-implement 2
/my-interface-implement 3
/my-interface-launch
```

Or run several phases together:

```text
/my-interface-implement 1 2 3
/my-interface-launch
```

Launch runs after all required phases are complete.



<br><br>

## Detailed

For direct control over every operation:

```text
/my-interface-configure
/my-interface-planning 1
/my-interface-developing 1
/my-interface-reviewer 1
If Review is not satisfied: run planning 1, developing 1, reviewer 1 again until it is
Repeat Planning, Developing, and Review for each remaining phase
/my-interface-launch
```

Planning defines the work, Development creates and verifies the implementation, and Review evaluates the resulting Plan coverage and implementation. A phase is reconciled before advancing, and Launch runs only after all required phases satisfy Review.

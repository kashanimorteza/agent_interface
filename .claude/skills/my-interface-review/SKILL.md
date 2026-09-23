---
name: my-interface-review
description: Core Interface Skill "Review" (stable key `review`). Independently judges each selected (or every) Target phase's Plan and implemented result against the current Interface, Target, and Plan; records grounded Findings in State Log Entries, resolves what it is authorized to resolve, and re-reviews until satisfied or blocked. Use after Development to verify a phase. Optional argument - one or more Target phase identifiers.
argument-hint: "[phase-id ...]"
---

# Review

The Core Skill for reviewing. Required. Stable key: `review`. Skill name: `my-interface-review`.

This Skill is a synchronized Runtime realization. It never reads, searches, or resolves the Agent Module; a missing or unusable Runtime capability is reported as Runtime drift and the Human is asked to run Agent Native Sync.

## Contract

- **Inputs:** an invocation request and an optional phase selection (`$ARGUMENTS`: zero or more Target phase identifiers).
- **Invocation:** may be invoked directly by a Human (`/my-interface-review`) or by an Agent (Skill tool).
- **Requirements:** a successful Configure execution must have established the required Config records before this Skill runs. Each selected phase must have a current Plan and a Development result.
- **Outputs:** the Skill execution result and status.

## Start of workflow

1. Apply the Runtime Rules `interface-bootstrap` and `interface-skill-policy` (`.claude/rules/`) before anything else.
2. Locate through the Interface, then read completely, the current **Review Operation Component** Definition and Preferences (currently `.interface/implementation/operations/review/review.md` and `review.yaml`). They are the authority; this file only summarizes them, and on any difference the current sources win.

## Procedure

1. Record the active Workflow position as `reviewing`.
2. **Phases.** Use the selected phase identifiers, or every phase when none is selected.
3. For each phase, once generated Source is available: establish current Target Understanding, Interface Understanding, and Source Understanding **within that phase's scope only**; read the current Plan.
4. **Pass.** Judge the generated Source, Public Interface, implemented result, and evidence against the current Plan and the same current authorities. Write one State Log Entry per pass, with its Findings in `data`.
5. **Resolve and recheck.** Resolve each Finding Review is authorized and able to resolve, record the resolution in a new Log Entry, then run another independent pass. Repeat until no Finding remains (outcome `satisfied`) or an unresolvable Finding is recorded in `open_questions` or `blockers` (stops the cycle).
6. Record the phase's aggregate Review outcome (`satisfied` / `not satisfied`) under State.

## Judgment rules

- **Independent:** observe each required condition yourself. Read the implementer's check and evidence, but judge whether that check actually establishes the condition — never accept "it passed" as proof.
- **Grounded:** every Finding states what was expected, what was observed, and the exact location or observable result that shows it. An untraceable concern is reported as an observation about the review, not recorded as a Finding.
- **Missing evidence is a Finding:** an acceptance criterion with nothing observable behind it is recorded as its own Finding. Never reconstruct, infer, or accept an explanation in place of evidence.
- **Persistent:** every Finding lives in the State Log `data` and stays traceable through the pass that raised it and any pass that resolved it or left it open.
- **Baseline only:** never define new requirements; silence in the baseline is a fact about the baseline, not a requirement. Newly required work belongs to Planning.

## Stop when

The required result or evidence is unavailable, an authority cannot be established, or an unresolved condition prevents assurance. Always report the reason.

## Never

- change Target meaning, Plan content, Task status, or any other Operation's owned record, or reopen Tasks;
- change anything except the reviewed implementation and the evidence needed to resolve one of its recorded Findings.

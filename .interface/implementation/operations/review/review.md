# Review Definition

Review is the Operation Component that independently judges selected-phase Plans and implemented results against their applicable authorities.

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

Review is the Operation Component that establishes whether a phase Plan and its implemented result satisfy the current Interface and Target, and records what it found.

Review owns its Findings and the Log data that records what was reviewed. It does not own Plan or Target. When it runs, it records the active Workflow position as `reviewing`, then records aggregate Review progress and its outcome under State.

### Purpose

Review is the reader who does not hold the producer's intent. It takes the current authorities and Target, builds the obligations they impose, and judges the Plan and implemented result against them.

Review first records what it finds, then resolves the findings it is authorized and able to resolve. After each resolution it reviews the result again. A finding that cannot be resolved is retained in the Log Entry's `open_questions` or `blockers`.

### How It Works

Review accepts one or more Target phase identifiers, or considers every phase when none is selected. For each phase, it establishes current Target Understanding, Interface Understanding, and Source Understanding within that phase's scope. Once generated Source is available, it reads the current Plan and examines the generated Source, Public Interface, implemented result, and evidence against that Plan and the current authorities. Each Review execution uses one Log Entry: it records Findings in `data` and updates those same Findings when it resolves them. A later independent Review execution creates its own Log Entry.

Review stops when the required result or evidence is unavailable, an authority cannot be established, or an unresolved condition prevents assurance.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Review** — one independent examination of one phase's Plan and implemented result against the current Interface and Target.
- **Source Understanding** — understanding the generated Source needed to examine the selected phase without reading unrelated Source.
- **Finding** — one specific way in which the result does not demonstrably satisfy what was asked, recorded with what was expected, what was observed, and where.
- **Evidence** — the exact location or observable result that supports a finding, so that a reader can see it without repeating the review.
- **Outcome** — the aggregate result: `satisfied` when the reviewed result satisfies the current Plan and applicable authorities, or `not satisfied` otherwise.
- **Missing evidence** — an acceptance criterion for which nothing observable demonstrates that it holds.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Interface, Target, and Plan** — takes their current meaning, Plan coverage, acceptance criteria, and verification conditions as the baseline for a phase.
- **Consumes State** — uses current aggregate progress and prior Review Log Entries without treating either as authority.
- **Consumed by State** — writes the phase's aggregate Review outcome and a Log Entry containing execution metadata, a concise report, and Review-specific data including Findings and resolutions.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Review owns its Findings, review data, and the resolutions it can perform. Plan owns planned work and Develop owns implementation work outside Review's resolution scope.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principles in this Definition govern Review. Review Preferences cannot lower the evidence or independence required by those Principles.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Review examines Source against the current Plan and authorities

**Rule:** A Review accepts one or more Target phase identifiers, or considers every phase when none is selected. Once generated Source is available for a phase, it establishes current Target Understanding, Interface Understanding, and Source Understanding within that phase's scope. It reads the current Plan, then judges the generated Source, Public Interface, implemented result, and evidence against that Plan and the same current authorities.

**Why:** A result can only be wrong relative to a current intended outcome, its governing rules, and the work that was planned for it. Judging it against what the implementer intended, or against what a reviewer would have built, measures the wrong thing.

**Boundary:** Review does not define new requirements or change Plan content. Work newly required by Target belongs to Planning. When the authoritative baseline is silent about something, that silence is a fact about the baseline, not a licence to supply the missing requirement and then find the result wanting.

<br>

### Review records, resolves, and rechecks its findings

**Rule:** When Review begins, it records the active Workflow position as `reviewing`. It first records its Findings in its Log Entry, then updates those same Finding records when it resolves them. A Finding that cannot be resolved is recorded in `open_questions` or `blockers` and stops the cycle. A later independent Review execution records its work in a new Log Entry.

**Why:** Recording the Finding before resolving it preserves the original observation while allowing Review to close the loop and verify the result.

**Boundary:** Review may change only the reviewed implementation and the evidence needed to resolve one of its recorded Findings. It never changes Target meaning, Plan content, Task status, or any other Operation's owned record.

<br>

### Review is independent of how the work was done

**Rule:** Review observes the required condition for itself. It may read the check the implementer built and the evidence it recorded, but it judges whether that check actually establishes the condition rather than accepting that it passed.

**Why:** The same operation wrote the code and the check that proves it, so a check shaped around the implementation will pass whatever the implementation happens to do. Independence is the whole reason Review exists.

**Boundary:** Independence is about the judgment, not about the sources. Review uses current Target Understanding, applicable Interface Principles and Preferences, and the phase Plan; it does not invent a different standard.

<br>

### Every Finding is grounded in an observation

**Rule:** A Finding states what was expected, what was observed, and the exact location or observable result that shows it. A statement that cannot be traced to something a reader can see for themselves is not a Finding.

**Why:** A Finding is a claim about the project that someone will act on. Grounding it in an observation is what lets the human check it instead of trusting it.

**Boundary:** A concern that cannot be observed may still be worth saying, but it is said as an observation about the review itself, not recorded as a Finding.

<br>

### Missing evidence is a Finding, not an absence

**Rule:** When an acceptance criterion has nothing observable to demonstrate it, that is recorded as a Finding of its own. Review does not reconstruct the missing evidence, infer it from the implementation, or treat a plausible result as proof that a check once passed.

**Why:** Unproven and proven look identical in a record that only lists failures, and the difference between them is exactly what a review is for.

**Boundary:** Missing evidence describes what the record does not show. It is not a claim that the requirement is unmet, and it is not resolved by the implementer explaining what they did.

<br>

### A Finding outlives the session that raised it

**Rule:** Every Finding is stored in the Review Skill's State Log `data`, and remains traceable through the Entry that raised it, resolved it, or left it open. Its state is part of that Entry's data.

**Why:** A finding reported only in conversation is gone when the session ends, and the next run has no way to know it was ever raised. A stored finding is the only thing that makes the second review of a phase worth more than the first.

**Boundary:** Review records its Findings, resolutions, and aggregate outcome in its State Log Entries. It does not reopen Tasks or change Plan content.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Review examines Source against the current Plan and authorities**

- **Must** — accept one or more Target phases, or every phase when none is selected
- **Must** — establish Target, Interface, and Source Understanding for the selected phase once generated Source is available
- **Must** — judge generated Source, Public Interface, implementation, and evidence against the current Plan and authorities
- **Never** — Review defines a new requirement, changes Plan content, or treats silence in the baseline as a requirement

**Review records, resolves, and rechecks its findings**

- **Must** — record Findings before resolving them and update the same Finding records with each resolution
- **Must** — record the active Workflow position as `reviewing` when Review begins
- **Never** — Review writes Plan content, changes Target, or changes Task progress

**Review is independent of how the work was done**

- **Must** — Review observes the required condition for itself and judges whether the implementer's check establishes it
- **Never** — Review accepts that a check passed as proof that the condition holds

**Every Finding is grounded in an observation**

- **Must** — every Finding states what was expected, what was observed, and the exact evidence that shows it
- **Never** — an untraceable statement is recorded as a Finding

**Missing evidence is a Finding, not an absence**

- **Must** — an acceptance criterion with nothing observable behind it is recorded as a Finding of missing evidence
- **Never** — Review reconstructs missing evidence, infers it, or accepts an explanation in its place

**A Finding outlives the session that raised it**

- **Must** — every Finding is stored with its Review and keeps its state until resolved or accepted
- **Never** — Review reopens Tasks or changes Plan content

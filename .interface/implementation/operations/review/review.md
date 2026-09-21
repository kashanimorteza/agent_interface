# Review Definition

Review is the Operation Component that independently judges selected-phase Plans and available implementation against their applicable authorities.

Responsibility: The assurance of phase Plans and implemented results against their applicable authorities.

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

Review is the Component that establishes whether a phase Plan and, when implementation exists, its implemented result satisfy the current Interface and Target, and records what it found.

Review owns its Findings and the Log data that records what was reviewed. It does not own Plan, Target, or the active Workflow position, and it never enters or changes a Workflow Mode. It records aggregate Review progress and its Log outcome under State.

### Purpose

Review is the reader who does not hold the producer's intent. It takes the current authorities and Target, builds the obligations they impose, and judges the Plan and, when it exists, the implemented result against them.

Review first records what it finds, then resolves the findings it is authorized and able to resolve. After each resolution it reviews the result again. A finding that cannot be resolved is retained in the Log Entry's `open_questions` or `blockers`.

### How It Works

Review works one phase at a time from current authorities. It requires the selected Plan and available Development result, establishes the Plan as its baseline, then examines the generated Source, Public Interface, implemented result, and evidence against that baseline. It writes one Log Entry for every review pass, records its Findings in `data`, resolves what it can, and starts another pass until no Finding remains or a blocker prevents continuation.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Review** — one independent examination of one phase's Plan and, when present, implemented result against the current Interface and Target.
- **Plan Assurance** — the mandatory Review judgment that a phase Plan completely and correctly covers current Target Understanding and applicable Component authorities.
- **Assured Plan Revision** — the exact Plan Revision examined by Plan Assurance and stored with its outcome.
- **Review ID** — the stable identifier of the current Review invocation, recorded in its State Log data.
- **Implementation Assurance** — the conditional Review judgment that existing implementation and evidence satisfy the assured Plan and its current authorities.
- **Finding** — one specific way in which the result does not demonstrably satisfy what was asked, recorded with what was expected, what was observed, and where.
- **Evidence** — the exact location or observable result that supports a finding, so that a reader can see it without repeating the review.
- **Outcome** — the aggregate result: `satisfied` when Plan Assurance and Implementation Assurance pass, or the exact `not satisfied` or `inconclusive` result otherwise.
- **Missing evidence** — an acceptance criterion for which nothing observable demonstrates that it holds.
- **Gap** — required work that no planned activity covers, found by reviewing the phase rather than any one activity.

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Interface, Target, and Plan** — takes their current meaning, Plan coverage, acceptance criteria, and verification conditions as the baseline for a phase.
- **Consumes State** — uses current aggregate progress and prior Review Log Entries without treating either as authority.
- **Consumed by State** — writes the phase's aggregate Review outcome and a Log Entry containing execution metadata, a concise report, and Review-specific data including Findings and resolutions.

<br>

Technical choices and defaults belong to Review Preferences, which currently define none. Review results are stored in the State Log; Review has no separate generated Config record.

<br>

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

<!--------------------------------------------------------------------------------- Layering --->
<!--------------------------------------------------------------------------------- Layering --->
## Layering

Review owns assurance, Findings, and the resolutions it can perform. Plan owns planned work and Develop owns implementation work outside Review's resolution scope.

<br>

<!--------------------------------------------------------------------------------- Authority --->
<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principles and Operation Contract in this Definition govern Review. Review Preferences are empty and cannot lower the evidence or independence required by those Principles.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Review always assures the Plan before available implementation

**Rule:** A Review reconstructs current Interface Understanding and Target Understanding only after the selected Plan and Development result are available. It independently judges one phase's Plan against the current Target and every applicable Principle and Preference, records the exact Assured Plan Revision, and then judges the generated Source, Public Interface, implementation, and evidence against that assured Plan and the same current authorities.

**Why:** A result can only be wrong relative to something. Judging it against what the implementer intended, or against what a reviewer would have built, measures the wrong thing.

**Boundary:** Review does not define new requirements. A Plan Assurance outcome applies only to its recorded revision and becomes stale when the current Plan Revision differs. When the authoritative baseline is silent about something, that silence is a fact about the baseline, not a licence to supply the missing requirement and then find the Plan or result wanting.

<br>

### Review records, resolves, and rechecks its findings

**Rule:** Every Review pass first records its Findings, then resolves each Finding that Review is authorized and able to resolve. It records the resolution in a new Log Entry and runs another independent pass. A Finding that cannot be resolved is recorded in `open_questions` or `blockers` and stops the cycle.

**Why:** Recording the Finding before resolving it preserves the original observation while allowing Review to close the loop and verify the result.

**Boundary:** Review never changes Target meaning, Plan content, Task status, or another operation's owned records. Its resolution scope is limited to the reviewed implementation and the evidence needed to establish the result.

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

### A Finding is required work no activity covers

**Rule:** A Review may find that the phase requires something no planned activity covers. That is recorded as a Finding of the phase rather than of any activity, because it belongs to none.

**Why:** The most consequential thing a review can notice is what nobody thought to do, and a record that can only attach a Finding to an existing activity is structurally unable to hold it.

**Boundary:** Recording such a Finding does not authorize Review to create Plan content or invoke Plan. Review either resolves the issue within its scope or records the unresolved condition.

<br>

### A Finding outlives the session that raised it

**Rule:** Every Finding is stored in the Review Skill's State Log `data`, and remains traceable through the pass that raised it and any later pass that resolved it or left it open. Its state is part of the Log Entry data.

**Why:** A finding reported only in conversation is gone when the session ends, and the next run has no way to know it was ever raised. A stored finding is the only thing that makes the second review of a phase worth more than the first.

**Boundary:** Review records its Findings, resolutions, and aggregate outcome in its State Log Entries. It does not reopen Tasks, change Plan content, invoke another Operation Skill, or change the active Workflow mode to reflect what it found.

<br>

<!--------------------------------------------------------------------------------- Operation Contract --->
## Operation Contract

Review accepts zero or more phase selections. An empty selection means every enabled phase that has an implementation. It resolves stable phase identities, removes duplicates, and preserves Target order.

Review establishes fresh Interface Understanding and Target Understanding on every invocation. It reads the selected Plan, State, applicable Implementation authorities, synchronized Runtime rules, implementation, generated Source, public interfaces, prior Review Log Entries, and evidence. It never reads Agent Module sources.

Review independently compares the current Plan and implementation with those authorities. It produces Plan Assurance and Implementation Assurance for each reviewable phase, assigns a stable Review ID, records Review-owned Findings and resolutions, aggregate Review State and Log Entries, obligation coverage, and a phase report. A phase without a completed Plan and Development result is not reviewable and receives no assurance outcome.

Review writes one State Log Entry for every review pass. The entry stores the start and completion times, measurable duration, available operation-level token usage, the Skills actually used with their available metrics and reports, a concise summary of the assurance outcome, and Review-specific `data`. That data includes the reviewed phase and Plan Revision, both assurance outcomes, Finding identifiers, detailed evidence, and any resolution. Review has no separate generated Config record.

Review may use any supporting Skill and records the Skills it actually used. It never invokes another Operation Skill and never changes Plan content, Task progress, Target, or another operation's records. It repeats its own review after each resolution until the result is satisfied or an unresolved condition is recorded.

Review is idempotent and evidence-first. It stops on invalid selection, missing implementation or generated Source, inconclusive evidence, unavailable authority, or an unresolved condition that prevents assurance.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Review always assures the Plan before available implementation**

- **Must** — every Review reconstructs current Interface and Target Understanding and assures the selected phase's Plan before judging available generated Source, Public Interface, implementation, and evidence
- **Must** — record Plan Assurance and Implementation Assurance separately after the selected Plan and Development result are available
- **Must** — bind every Plan Assurance outcome to the exact Plan Revision it examined
- **Never** — Review defines a new requirement, or treats silence in the baseline as one

**Review records, resolves, and rechecks its findings**

- **Must** — record Findings before resolving them, record each resolution, and perform another pass after each resolution
- **Never** — Review writes Plan content, changes Target, changes Task progress, or invokes another Operation Skill

**Review is independent of how the work was done**

- **Must** — Review observes the required condition for itself and judges whether the implementer's check establishes it
- **Never** — Review accepts that a check passed as proof that the condition holds

**Every Finding is grounded in an observation**

- **Must** — every Finding states what was expected, what was observed, and the exact evidence that shows it
- **Never** — an untraceable statement is recorded as a Finding

**Missing evidence is a Finding, not an absence**

- **Must** — an acceptance criterion with nothing observable behind it is recorded as a Finding of missing evidence
- **Never** — Review reconstructs missing evidence, infers it, or accepts an explanation in its place

**A Finding is required work no activity covers**

- **Must** — required work that no planned activity covers is recorded as a Finding of the phase
- **Never** — Review plans the work that would fill a gap it found

**A Finding outlives the session that raised it**

- **Must** — every Finding is stored with its Review and keeps its state until resolved or accepted
- **Never** — Review reopens Tasks, changes Plan content, or changes the active Workflow mode

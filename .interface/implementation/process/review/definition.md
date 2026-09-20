# Review Definition

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[Review always assures the Plan before available implementation](#review-always-assures-the-plan-before-available-implementation)**
   - **[Review passes report; reconciliation stays with the owning operation](#review-passes-report-reconciliation-stays-with-the-owning-operation)**
   - **[Review is independent of how the work was done](#review-is-independent-of-how-the-work-was-done)**
   - **[Every Finding is grounded in an observation](#every-finding-is-grounded-in-an-observation)**
   - **[Missing evidence is a Finding, not an absence](#missing-evidence-is-a-finding-not-an-absence)**
   - **[A Finding is required work no activity covers](#a-finding-is-required-work-no-activity-covers)**
   - **[A Finding outlives the session that raised it](#a-finding-outlives-the-session-that-raised-it)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Review is the Component that establishes whether a phase Plan and, when implementation exists, its implemented result satisfy the current Interface and Target, and records what it found.

Review owns its Findings and the record of what was reviewed. It does not own implementation, Plan, Target, or the active Workflow position, and it never enters or changes a Workflow Mode. It records only aggregate Review progress and its History outcome under State.

### Purpose

Review is the reader who does not hold the producer's intent. It takes the current authorities and Target, builds the obligations they impose, and judges the Plan and, when it exists, the implemented result against them.

What makes it useful is that it only judges. It reconciles nothing and fixes nothing: each Finding names the operation that owns the work, and that operation resolves it. A judge who also repairs stops being independent by the second repair, and the record of what was wrong disappears into the fix.

### How It Works

Review works one phase at a time from current authorities. It establishes the Plan as its baseline, then, when available, examines the generated Source, Public Interface, implemented result, and evidence against that baseline. It records the outcome and any Finding for the operation that owns its resolution.

<br>

## Terms

- **Review** — one independent examination of one phase's Plan and, when present, implemented result against the current Interface and Target.
- **Plan Assurance** — the mandatory Review judgment that a phase Plan completely and correctly covers current Target Understanding and applicable Component authorities.
- **Assured Plan Revision** — the exact Plan Revision examined by Plan Assurance and stored with its outcome.
- **Implementation Assurance** — the conditional Review judgment that existing implementation and evidence satisfy the assured Plan and its current authorities.
- **Finding** — one specific way in which the result does not demonstrably satisfy what was asked, recorded with what was expected, what was observed, and where.
- **Evidence** — the exact location or observable result that supports a finding, so that a reader can see it without repeating the review.
- **Outcome** — the aggregate result: `plan satisfied` when Plan Assurance passes and implementation is not yet available, `satisfied` when both applicable assurances pass, or the exact `not satisfied` or `inconclusive` result otherwise.
- **Missing evidence** — an acceptance criterion for which nothing observable demonstrates that it holds.
- **Gap** — required work that no planned activity covers, found by reviewing the phase rather than any one activity.

## Relationships

- **Consumes Interface, Target, and Plan** — takes their current meaning, Plan coverage, acceptance criteria, and verification conditions as the baseline for a phase.
- **Consumes State** — uses current aggregate progress and prior Review records without treating either as authority.
- **Consumed by Plan** — a recorded Gap identifies work the Plan must cover without copying the Finding into Plan content.
- **Consumed by State** — provides the phase's aggregate Review outcome and a concise History event; Findings remain Review-owned.

<br>

Technical choices and defaults belong to Review Preferences, which currently define none. The exact shape of the generated Review configuration belongs to the Review Schema.

<br>

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

## Principles

Every Principle below is mandatory.

<br>

### Review always assures the Plan before available implementation

**Rule:** A Review reconstructs current Interface Understanding and Target Understanding, then independently judges one phase's Plan against the current Target and every applicable Principle and Preference. It records the exact Assured Plan Revision with the Plan Assurance outcome. Only after Plan Assurance is satisfied does it judge the generated Source, Public Interface, existing implementation, and evidence against that assured Plan and the same current authorities. When no implementation exists, Implementation Assurance is explicitly `not reviewed` rather than inferred.

**Why:** A result can only be wrong relative to something. Judging it against what the implementer intended, or against what a reviewer would have built, measures the wrong thing.

**Boundary:** Review does not define new requirements. A Plan Assurance outcome applies only to its recorded revision and becomes stale when the current Plan Revision differs. When the authoritative baseline is silent about something, that silence is a fact about the baseline, not a licence to supply the missing requirement and then find the Plan or result wanting.

<br>

### Review passes report; reconciliation stays with the owning operation

**Rule:** An individual Review pass changes no implementation, Plan, Target definition, or Task progress. It records a Finding for the operation that owns any missing, stale, incomplete, or invalid result; Review never repairs implementation.

**Why:** An operation that fixes what it finds loses the ability to tell the difference between what was already correct and what it corrected, and the human never learns that the problem existed.

**Boundary:** Recording or reconciling a Finding and re-running a check are not repairs. Planning remains the sole writer of Planning-owned content, and Review must preserve evidence of the original Plan Finding before independently judging the reconciled Plan.

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

**Boundary:** Recording such a Finding is not planning. Review names what is missing; deciding the work that fills it belongs to Planning.

<br>

### A Finding outlives the session that raised it

**Rule:** Every Finding is stored with its Review, and remains stored until an authorized Review establishes that it no longer holds or the human accepts it as it is. Its state is part of the record.

**Why:** A finding reported only in conversation is gone when the session ends, and the next run has no way to know it was ever raised. A stored finding is the only thing that makes the second review of a phase worth more than the first.

**Boundary:** Review records its Findings and its own aggregate outcome under State. It does not reopen Tasks, raise Blockers on another Component's behalf, or change the active Workflow mode to reflect what it found.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Review always assures the Plan before available implementation**

- **Must** — every Review reconstructs current Interface and Target Understanding and assures the selected phase's Plan before judging available generated Source, Public Interface, implementation, and evidence
- **Must** — record Plan Assurance and Implementation Assurance separately, using `not reviewed` when implementation does not exist
- **Must** — bind every Plan Assurance outcome to the exact Plan Revision it examined
- **Never** — Review defines a new requirement, or treats silence in the baseline as one

**Review passes report; reconciliation stays with the owning operation**

- **Must** — a Review pass changes nothing it judges; every Finding names its owning operation and a reconciled Plan receives a new independent pass
- **Never** — Review writes Plan content, repairs implementation, changes Target, or changes Task progress

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
- **Never** — Review reopens Tasks, raises Blockers for another Component, or changes the active Workflow mode

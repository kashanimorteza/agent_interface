# Review Principles

Review is the Component that establishes whether a phase Plan and, when implementation exists, its implemented result satisfy the current Interface and Target, and records what it found. It exists because the operation that produces a Plan or result is the worst judge of it: the producer knows what it meant to create, and that knowledge quietly fills the gaps that an independent reader would notice.

Review owns its Findings and the record of what was reviewed. It does not own implementation, Plan, Target, or the active Workflow position, and it never enters or changes a Workflow Mode. It records only aggregate Review progress and its History outcome under State.

## Terms

- **Review** — one independent examination of one phase's Plan and, when present, implemented result against the current Interface and Target.
- **Plan Assurance** — the mandatory Review judgment that a phase Plan completely and correctly covers current Target Understanding and applicable Component authorities.
- **Implementation Assurance** — the conditional Review judgment that existing implementation and evidence satisfy the assured Plan and its current authorities.
- **Finding** — one specific way in which the result does not demonstrably satisfy what was asked, recorded with what was expected, what was observed, and where.
- **Evidence** — the exact location or observable result that supports a finding, so that a reader can see it without repeating the review.
- **Outcome** — the aggregate result: `plan satisfied` when Plan Assurance passes and implementation is not yet available, `satisfied` when both applicable assurances pass, or the exact `not satisfied` or `inconclusive` result otherwise.
- **Missing evidence** — an acceptance criterion for which nothing observable demonstrates that it holds.
- **Gap** — required work that no planned activity covers, found by reviewing the phase rather than any one activity.

## Relationships

- **Consumes Interface and Target Understanding** — reconstructs both from current sources before judging a phase.
- **Consumes Plan** — the Plans, acceptance criteria, verification conditions, and recorded execution evidence a result is judged against.
- **Consumed by Plan** — a Finding recorded as a gap names required work that no planned activity covers, and Planning is where that work is decided.
- **Updates State** — records the phase's aggregate Review outcome and a concise History event without copying Findings.

Technical choices and defaults belong to Review Preferences, which currently define none. The exact shape of the generated Review configuration belongs to the Review Schema.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Review always assures the Plan before available implementation

**Rule:** A Review reconstructs current Interface Understanding and Target Understanding, then independently judges one phase's Plan against the current Target and every applicable Principle and Preference. Only after Plan Assurance is satisfied does it judge existing implementation and evidence against that assured Plan and the same current authorities. When no implementation exists, Implementation Assurance is explicitly `not reviewed` rather than inferred.

**Why:** A result can only be wrong relative to something. Judging it against what the implementer intended, or against what a reviewer would have built, measures the wrong thing.

**Boundary:** Review does not define new requirements. When the authoritative baseline is silent about something, that silence is a fact about the baseline, not a licence to supply the missing requirement and then find the Plan or result wanting.

<br>

## 2. Review passes report; reconciliation stays with the owning operation

**Rule:** An individual Review pass changes no implementation, Plan, Target definition, or Task progress. The Reviewing Skill may coordinate Planning for the same phase when Plan Assurance exposes a missing, stale, incomplete, or invalid Plan, then perform a new independent Review pass against Planning's result. It never invokes Development or repairs implementation.

**Why:** An operation that fixes what it finds loses the ability to tell the difference between what was already correct and what it corrected, and the human never learns that the problem existed.

**Boundary:** Recording or reconciling a Finding and re-running a check are not repairs. Planning remains the sole writer of Planning-owned content, and Review must preserve evidence of the original Plan Finding before independently judging the reconciled Plan.

<br>

## 3. Review is independent of how the work was done

**Rule:** Review observes the required condition for itself. It may read the check the implementer built and the evidence it recorded, but it judges whether that check actually establishes the condition rather than accepting that it passed.

**Why:** The same operation wrote the code and the check that proves it, so a check shaped around the implementation will pass whatever the implementation happens to do. Independence is the whole reason Review exists.

**Boundary:** Independence is about the judgment, not about the sources. Review uses current Target Understanding, applicable Interface Principles and Preferences, and the phase Plan; it does not invent a different standard.

<br>

## 4. Every Finding is grounded in an observation

**Rule:** A Finding states what was expected, what was observed, and the exact location or observable result that shows it. A statement that cannot be traced to something a reader can see for themselves is not a Finding.

**Why:** A Finding is a claim about the project that someone will act on. Grounding it in an observation is what lets the human check it instead of trusting it.

**Boundary:** A concern that cannot be observed may still be worth saying, but it is said as an observation about the review itself, not recorded as a Finding.

<br>

## 5. Missing evidence is a Finding, not an absence

**Rule:** When an acceptance criterion has nothing observable to demonstrate it, that is recorded as a Finding of its own. Review does not reconstruct the missing evidence, infer it from the implementation, or treat a plausible result as proof that a check once passed.

**Why:** Unproven and proven look identical in a record that only lists failures, and the difference between them is exactly what a review is for.

**Boundary:** Missing evidence describes what the record does not show. It is not a claim that the requirement is unmet, and it is not resolved by the implementer explaining what they did.

<br>

## 6. A Finding is required work no activity covers

**Rule:** A Review may find that the phase requires something no planned activity covers. That is recorded as a Finding of the phase rather than of any activity, because it belongs to none.

**Why:** The most consequential thing a review can notice is what nobody thought to do, and a record that can only attach a Finding to an existing activity is structurally unable to hold it.

**Boundary:** Recording such a Finding is not planning. Review names what is missing; deciding the work that fills it belongs to Planning.

<br>

## 7. A Finding outlives the session that raised it

**Rule:** Every Finding is stored with its Review, and remains stored until an authorized Review establishes that it no longer holds or the human accepts it as it is. Its state is part of the record.

**Why:** A finding reported only in conversation is gone when the session ends, and the next run has no way to know it was ever raised. A stored finding is the only thing that makes the second review of a phase worth more than the first.

**Boundary:** Review records its Findings and its own aggregate outcome under State. It does not reopen Tasks, raise Blockers on another Component's behalf, or change the active Workflow mode to reflect what it found.

<br>

## At a Glance

- **Must** — every Review reconstructs current Interface and Target Understanding and assures the selected phase's Plan before judging available implementation *(1)*
- **Must** — record Plan Assurance and Implementation Assurance separately, using `not reviewed` when implementation does not exist *(1)*
- **Never** — Review defines a new requirement, or treats silence in the baseline as one *(1)*
- **Must** — a Review pass changes nothing it judges; Plan reconciliation is delegated to Planning and followed by a new independent pass *(2)*
- **Never** — Review writes Plan content, repairs implementation, changes Target, or changes Task progress *(2)*
- **Must** — Review observes the required condition for itself and judges whether the implementer's check establishes it *(3)*
- **Never** — Review accepts that a check passed as proof that the condition holds *(3)*
- **Must** — every Finding states what was expected, what was observed, and the exact evidence that shows it *(4)*
- **Never** — an untraceable statement is recorded as a Finding *(4)*
- **Must** — an acceptance criterion with nothing observable behind it is recorded as a Finding of missing evidence *(5)*
- **Never** — Review reconstructs missing evidence, infers it, or accepts an explanation in its place *(5)*
- **Must** — required work that no planned activity covers is recorded as a Finding of the phase *(6)*
- **Never** — Review plans the work that would fill a gap it found *(6)*
- **Must** — every Finding is stored with its Review and keeps its state until resolved or accepted *(7)*
- **Never** — Review reopens Tasks, raises Blockers for another Component, or changes the active Workflow mode *(7)*

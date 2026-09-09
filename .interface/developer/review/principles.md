# Review Principles

Review is the Component that establishes whether an implemented result satisfies what the project asked for, and records what it found. It exists because the operation that produces a result is the worst judge of it: the implementer knows what it meant to build, and that knowledge quietly fills the gaps that an independent reader would notice.

Review owns its findings and the record of what was reviewed. It does not own the implementation, the Plan, the project definition, or the Workflow position, and it never enters or changes a Workflow Mode.

## Terms

- **Review** — one examination of one phase's implemented result against what that phase was asked to produce.
- **Finding** — one specific way in which the result does not demonstrably satisfy what was asked, recorded with what was expected, what was observed, and where.
- **Evidence** — the exact location or observable result that supports a finding, so that a reader can see it without repeating the review.
- **Outcome** — the reviewed scope's overall result: whether it satisfies what was asked, does not, or cannot be established.
- **Missing evidence** — an acceptance criterion for which nothing observable demonstrates that it holds.
- **Gap** — required work that no planned activity covers, found by reviewing the phase rather than any one activity.

## Relationships

- **Consumes Plan** — the Plans, acceptance criteria, verification conditions, and recorded execution evidence a result is judged against.
- **Consumed by Plan** — a Finding recorded as a gap names required work that no planned activity covers, and Planning is where that work is decided.

Technical choices and defaults belong to Review Preferences, which currently define none. The exact shape of the generated Review configuration belongs to the Review Schema.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Review judges the result against what was asked

**Rule:** A Review examines one phase's implemented result against the project definition, the applicable Principles and Preferences, and that phase's Plan and acceptance criteria. Those sources are the baseline, and nothing else is.

**Why:** A result can only be wrong relative to something. Judging it against what the implementer intended, or against what a reviewer would have built, measures the wrong thing.

**Boundary:** Review does not define new requirements. When the baseline is silent about something, that silence is a fact about the baseline, not a licence to supply the missing requirement and then find the result wanting.

<br>

## 2. Review reports and never repairs

**Rule:** Review records what it found and stops there. It changes no implementation, no Plan, no project definition, and no Task progress.

**Why:** An operation that fixes what it finds loses the ability to tell the difference between what was already correct and what it corrected, and the human never learns that the problem existed.

**Boundary:** Recording a Finding is not a repair, and neither is re-running a check. Nothing else Review does may change the thing it is judging.

<br>

## 3. Review is independent of how the work was done

**Rule:** Review observes the required condition for itself. It may read the check the implementer built and the evidence it recorded, but it judges whether that check actually establishes the condition rather than accepting that it passed.

**Why:** The same operation wrote the code and the check that proves it, so a check shaped around the implementation will pass whatever the implementation happens to do. Independence is the whole reason Review exists.

**Boundary:** Independence is about the judgment, not about the sources. Review uses the same project definition, Principles, Preferences, and Plan the implementer used; it does not invent a different standard.

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

**Boundary:** Review records the state of its own Findings and nothing else. It does not reopen Tasks, raise Blockers on another Component's behalf, or change the Workflow position to reflect what it found.

<br>

## At a Glance

- **Must** — a Review judges a phase's result against the project definition, the applicable Principles and Preferences, and that phase's Plan and acceptance criteria *(1)*
- **Never** — Review defines a new requirement, or treats silence in the baseline as one *(1)*
- **Must** — Review records what it found and changes nothing it is judging *(2)*
- **Never** — Review repairs an implementation, a Plan, a project definition, or Task progress *(2)*
- **Must** — Review observes the required condition for itself and judges whether the implementer's check establishes it *(3)*
- **Never** — Review accepts that a check passed as proof that the condition holds *(3)*
- **Must** — every Finding states what was expected, what was observed, and the exact evidence that shows it *(4)*
- **Never** — an untraceable statement is recorded as a Finding *(4)*
- **Must** — an acceptance criterion with nothing observable behind it is recorded as a Finding of missing evidence *(5)*
- **Never** — Review reconstructs missing evidence, infers it, or accepts an explanation in its place *(5)*
- **Must** — required work that no planned activity covers is recorded as a Finding of the phase *(6)*
- **Never** — Review plans the work that would fill a gap it found *(6)*
- **Must** — every Finding is stored with its Review and keeps its state until resolved or accepted *(7)*
- **Never** — Review reopens Tasks, raises Blockers for another Component, or changes the Workflow position *(7)*

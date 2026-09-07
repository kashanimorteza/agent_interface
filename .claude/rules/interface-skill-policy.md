# Agent Interface Skill policy

These shared rules apply to every Agent Interface Skill and supporting agent, including one written later. Each of them reads these rules at the start of its own Workflow, located through the Interface document, and none of them copies any part of them into its own instructions: a copied rule is a second version that drifts, and changing the rule would then mean editing every Skill that holds a copy.

## Human-owned files

Skills and supporting agents must never edit or delete a human-owned Interface source. The Interface document states which sources those are, and a YAML source additionally declares it in its own policy. Resolve the current set from there rather than from a list held here, because a list of paths goes stale the moment a source is renamed or added, and a stale list leaves a source unprotected without anyone noticing.

Only a human edits these sources. When a change appears necessary, report it and leave the source unchanged.

## Related capabilities

Check the Skills and capabilities already available in the environment for relevance to the current work. When applicable, read their instructions and use them within the active role and requested scope, respecting the project's resolved decisions and the current write boundaries.

When a relevant Skill recommends an alternative to the project's current choice, briefly explain the current choice, the proposed alternative, which Skill recommends it, and the reason for the recommendation. Ask the human whether to keep the current choice or adopt the alternative. Do not change the choice or proceed with work that depends on that decision until the human answers; independent work may continue. Apply an accepted alternative within the current role and write boundaries, reporting any required changes to human-owned sources.

## Decision policy

- Explicit project decisions, the applicable Principles, the declared interfaces between Components, permissions, and write boundaries are binding. They constrain professional judgment rather than being weighed against it: judgment settles what is undecided, never whether a decided thing still applies.
- When a necessary detail is not defined, choose the approach that best fits what is already binding, using the current role sources, available evidence, and professional judgment, then continue without asking. Record a choice that another operation would have to live with — a resolved technology, an interface shape, a stored structure — where that operation will find it, so that a decision made in passing does not later read as something the project always intended.
- A differing Skill recommendation requires the human decision described above. Otherwise, stop only when no safe choice can be made without materially affecting project intent, core architecture, security, data integrity, permissions, a declared interface, or an irreversible action. Stopping means recording the reason where the Workflow keeps it — a Blocker for a condition that prevents continuation, an Open Question for a decision only the human can make — and then reporting it. A question asked only in conversation is lost the moment the session ends, and the next run has no way to know it was ever raised.
- Discretion never expands the active role, requested scope, or write authority. All three are fixed at invocation — the role by the Skill selected, the scope by what was asked for, the authority by the Component that owns the record — so none of them is something an operation discovers midway and grants itself. Work that turns out to be necessary but lies outside them is reported as necessary, not performed.

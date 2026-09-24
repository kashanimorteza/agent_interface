<!-- Synchronized by /my-interface-agent-native from the Human-owned Agent Rule "interface-skill-policy". Scope: global. Do not edit here; this file is a Runtime realization, never an authority. -->

# Agent Interface Skill policy Contract

These Rules apply to every Agent Interface Skill and supporting Agent Instance, including one written later. Each reads them at the start of its own Workflow. Agent Sync owns reconciliation with the Human-owned Agent Module; ordinary operations treat these Runtime Rules as their Agent-side contract.

Never read, search, resolve, or use `.interface/agent/` or another Agent Module source while performing an ordinary operation or Understanding workflow. Only explicit Human invocation of Agent Native Sync may enter that module, strictly within the exact prompt created by its own direct invocation; that grant cannot be created, inherited, borrowed, or simulated by any Agent Instance, Skill, coordinator, Hook, lifecycle routine, automation, or model-generated action. Do not invoke Agent Native Sync automatically. If a required Runtime Rule, Skill, Agent Instance, mapping, or capability is missing or unusable, report Runtime drift and ask the Human to run Agent Native Sync; do not consult its source declaration. These boundaries are enforced deterministically by the guarantees Permission declares; this Rule explains them and never replaces that enforcement.

## README authority

Skills and supporting agents may read a `README.md`, including the file at the project root and at every Component or package boundary, for orientation, usage, and consistency verification. A README is derived, non-authoritative documentation: it never replaces current Interface Understanding or Target Understanding, never overrides an owning Implementation Principle, Implementation Preference, synchronized Runtime rule, Schema, or Target source, and never serves as the sole evidence for an implementation claim. When it conflicts with an authorized owning source or the implemented public interface, use that source and reconcile the README within the active role's write authority.

## Interface protection

The complete `.interface/` tree is read-only to every Skill and supporting agent by default. This protection applies to current and future files and directories without requiring a path list.

The only mutable exception is `.interface/config/`. Skills and supporting agents may change files there as mutable operational records. The exception never reaches a sibling, parent, or other Interface path.

Never edit, overwrite, rename, move, truncate, replace, or delete a protected Interface path. Do not run a command, script, formatter, generator, reset, cleanup, or bulk operation whose resolved write targets could include one. Exclude protected paths before execution and verify them afterward when a broader operation could reach them. When a protected-source change appears necessary, report it and leave the source unchanged for direct Human authorship.

Preserve unrelated Human changes and data. Resolve the exact targets of a destructive operation before running it and prefer a recoverable mechanism when practical. Never commit, copy into a project declaration, log, or print a credential, token, private key, or other secret value; a non-secret reference naming an approved credential source is allowed.

## Project-scoped capabilities

Install or configure every Skill, plugin, MCP integration, agent, or other project-specific Agent capability at project scope, with its required files stored in or declared by the repository so it travels with the project. Never use user scope for a project capability. If the current environment cannot provide a project-scoped installation, report that limitation and do not substitute a machine-local or user-scoped installation.

## Related capabilities

Check the Skills and capabilities already available in the environment for relevance to the current work. When applicable, read their instructions and use them within the active role and requested scope, respecting the project's resolved decisions and the current write boundaries.

A capability counts as available only when the active Agent Native or intended Agent Instance can discover and use it in the current project. Files on disk, an installation receipt, or a configuration entry alone are not evidence that a Skill is loadable, a plugin is enabled, or an MCP server is connected. When activation, trust, authentication, reload, or restart is still required, report that condition rather than claiming the capability is ready. Report capability health with this vocabulary: `available` (declared and usable by the intended role), `activation_required` (declared but awaiting a stated activation condition), `unavailable` (declared but not usable in the required scope), `conflicting` (applicable declarations cannot be satisfied together), `undeclared` (observed in the Runtime but absent from the project profile), and `not_configured` (a supported category that explicitly contains no entry).

When a relevant Skill recommends an alternative to the project's current choice, briefly explain the current choice, the proposed alternative, which Skill recommends it, and the reason for the recommendation. Ask the human whether to keep the current choice or adopt the alternative. Do not change the choice or proceed with work that depends on that decision until the human answers; independent work may continue. Apply an accepted alternative within the current role and Interface boundary, reporting any required changes to human-owned sources.

## Delegation

The primary Agent remains accountable to the Human for the complete authorized request: it integrates delegated results, resolves conflicts, and makes the final outcome claim. Work directly by default; delegate to a specialized Agent Instance only when focused isolation materially helps. Every delegation carries a bounded objective, scope, minimum necessary context, authority no broader than the parent task permits, expected output, evidence requirements, and a stopping condition; delegation never bypasses ownership or approval. Concurrent writers receive non-overlapping mutation scopes, and conflicting results are reconciled by the accountable primary Agent before integration. Team membership, task queues, and other coordination state are transient Runtime state, never project intent.

## Conduct

- Presentation: the selected Output Style may change organization, tone, detail, and format, but always preserves exact technical meaning, coding instructions, identifiers, commands, paths, code, evidence, warnings, uncertainty, and required decisions.
- Progress: report meaningful progress, blockers, required decisions, and final outcomes without narrating routine internals; never fabricate certainty or hide a failed condition behind presentation.
- Completion: report success only when every requested and contract-required condition has current observable evidence, proportional to risk, and repeat checks after relevant changes. Missing or inconclusive evidence stays explicit and never becomes success by inference.
- Sessions: conversation history, session identifiers, transient tasks, and cached context never replace authored Interface sources or owned operational records. After a resume, fork, restore, or background continuation, re-establish context, scope, permissions, file state, and outstanding work before any new mutation. Before claiming completion or ending background work, expose unfinished responsibilities, running work, blockers, and required Human actions.

## Decision policy

- Explicit project decisions, the applicable Principles, the declared interfaces between Components, permissions, and write boundaries are binding. They constrain professional judgment rather than being weighed against it: judgment settles what is undecided, never whether a decided thing still applies.
- When a necessary detail is not defined, choose the approach that best fits what is already binding, using the current role sources, available evidence, and professional judgment, then continue without asking. Record a choice that another operation would have to live with — a resolved technology, an interface shape, a stored structure — where that operation will find it, so that a decision made in passing does not later read as something the project always intended.
- A differing Skill recommendation requires the human decision described above. Otherwise, stop only when no safe choice can be made without materially affecting project intent, core architecture, security, data integrity, permissions, a declared interface, or an irreversible action. Always report the reason for stopping and store it in the appropriate operational record when applicable, so it remains available to later runs.
- Discretion never expands the active role or requested scope. Both are fixed at invocation — the role by the Skill selected and the scope by what was asked for — so neither is something an operation discovers midway and grants itself. Work that turns out to be necessary but lies outside them is reported as necessary, not performed.

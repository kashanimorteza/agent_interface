# Agent Interface Skill policy Contract

These Rules apply to every Agent Interface Skill and supporting Agent Instance, including one written later. Each reads them at the start of its own Workflow. Agent Sync owns reconciliation with the Human-owned Agent Module; ordinary operations treat these Runtime Rules as their Agent-side contract.

Never read, search, resolve, or use `.interface/agent/` or another Agent Module source while performing an ordinary operation or Understanding workflow. Only explicit Human invocation of Agent Native Sync may enter that module, strictly within the exact prompt created by its own direct invocation; that grant cannot be created, inherited, borrowed, or simulated by any Agent Instance, Skill, coordinator, Hook, lifecycle routine, automation, or model-generated action. Do not invoke Agent Native Sync automatically. If a required Runtime Rule, Skill, Agent Instance, mapping, or capability is missing or unusable, report Runtime drift and ask the Human to run Agent Native Sync; do not consult its source declaration. These boundaries are enforced deterministically by the guarantees Permission declares; this Rule explains them and never replaces that enforcement.

## README authority

Skills and supporting agents may read a `README.md`, including the file at the project root and at every Component or package boundary, for orientation, usage, and consistency verification. A README is derived, non-authoritative documentation: it never replaces current Interface Understanding or Target Understanding, never overrides an owning Implementation Principle, Implementation Preference, synchronized Runtime rule, Schema, or Target source, and never serves as the sole evidence for an implementation claim. When it conflicts with an authorized owning source or the implemented public interface, use that source and reconcile the README within the active role's write authority.

## Interface protection

The complete `.interface/` tree is read-only to every Skill and supporting agent by default. This protection applies to current and future files and directories without requiring a path list.

Config records live in `config/` at the project root, outside `.interface/`. Skills and supporting agents may change files there as mutable operational records.

Never edit, overwrite, rename, move, truncate, replace, or delete a protected Interface path. Do not run a command, script, formatter, generator, reset, cleanup, or bulk operation whose resolved write targets could include one. Exclude protected paths before execution and verify them afterward when a broader operation could reach them. When a protected-source change appears necessary, report it and leave the source unchanged for direct Human authorship.

Preserve unrelated Human changes and data. Resolve the exact targets of a destructive operation before running it and prefer a recoverable mechanism when practical. Never commit, copy into a project declaration, log, or print a credential, token, private key, or other secret value; a non-secret reference naming an approved credential source is allowed.

## Project-scoped capabilities

Install or configure every Skill, plugin, MCP integration, agent, or other project-specific Agent capability at project scope, with its required files stored in or declared by the repository so it travels with the project. Never use user scope for a project capability. If the current environment cannot provide a project-scoped installation, report that limitation and do not substitute a machine-local or user-scoped installation.

## Related capabilities

Check the Skills and capabilities already available in the environment for relevance to the current work. When applicable, read their instructions and use them within the active role and requested scope, respecting the project's resolved decisions and the current write boundaries.

A capability counts as available only when the active Agent Native or intended Agent Instance can discover and use it in the current project. Files on disk, an installation receipt, or a configuration entry alone are not evidence that a Skill is loadable, a plugin is enabled, or an MCP server is connected. When activation, trust, authentication, reload, or restart is still required, report that condition rather than claiming the capability is ready. Report capability health with the controlled Capability Status vocabulary.

When a relevant Skill recommends an alternative to the project's current choice, continue with the current choice and record the recommendation as an Open Question naming the Skill, the alternative, and its reason, so the Human can decide later.

## Delegation

The primary Agent remains accountable to the Human for the complete authorized request: it integrates delegated results, resolves conflicts, and makes the final outcome claim. Work directly by default; delegate to a specialized Agent Instance only when focused isolation materially helps. Every delegation carries a bounded objective, scope, minimum necessary context, authority no broader than the parent task permits, expected output, evidence requirements, and a stopping condition; delegation never bypasses ownership or approval. Concurrent writers receive non-overlapping mutation scopes, and conflicting results are reconciled by the accountable primary Agent before integration. Team membership, task queues, and other coordination state are transient Runtime state, never project intent.

## Decision policy

- Explicit project decisions, the applicable Principles, the declared interfaces between Components, permissions, and write boundaries are binding; judgment settles only what is undecided.
- An unstated choice is resolved under the precedence its owning authority declares, without stopping or asking, and the decision is recorded where that authority keeps it.
- Stop only on a condition other than an unstated choice, such as a conflict between binding sources, a missing required source, or a denied permission, and report the reason in the appropriate operational record.
- Discretion never expands the active role or requested scope, both fixed at invocation; necessary work outside them is reported, not performed.

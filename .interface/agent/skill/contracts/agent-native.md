# agent-native Skill Contract

This Skill is the Agent Native configuring itself from the Agent Module. It has three modes, given as a number: `1` sync self, `2` sync component, `3` install. Modes `1` and `2` are Agent Sync as defined throughout the Interface; mode `3` is the former Skill Installer operation, merged into this Skill on 2026-09-17. The name `agent-native` names the Skill and its entry point; the term Agent Native in Interface prose still means the core operational Agent supplied by the Runtime, which is what runs this Skill.

## Purpose

Reconstruct the complete Agent Module and realize it in the compatible project-scoped Agent Runtime.

In mode `3`: materialize the Prepared and Installed capabilities the Agent Module declares, and discover and provision additional ones, always through an explicit, auditable Human decision.

## Responsibility

Establish Interface Understanding, understand the complete Agent Module, learn the selected Agent Native's own documented capabilities and conventions, realize this Skill's own adapter in mode `1` (sync self) and every other declaration in mode `2` (sync component), translating the Module into that Native Runtime under the invoked mode. Reconcile authorized project artifacts and already-selected capabilities and prove complete availability. Agent Sync applies existing Human choices; it never discovers or selects new ones. Report an undeclared need for Human declaration and for mode `3` (install) of this Skill instead of adopting it here.

**Mode `3` (install).** Derive capability needs from current Target and synchronized Runtime evidence, discover compatible project-scoped candidates, preview provenance and impact, provision only approved candidates, and verify Activation. It manages Runtime capabilities, never application dependencies, Target implementation, or Agent Module declarations. It owns every capability the Module declares as Prepared or Installed: Prepared content is transferred into the Runtime unchanged, and an Installed capability is provisioned through its owning provider declaration. The sync modes build only Constructed Skills and materialize neither kind.

## Trigger

Activate only when the Human directly invokes the declared Runtime entry point while setting up, repairing, migrating, updating, or auditing an Agent Runtime. The Agent Native, every Agent Instance, Skill, coordinator, Hook, startup or resume routine, automation, and model-generated action are forbidden from invoking, chaining, triggering, or simulating this Skill. A Human request to change Agent Module declarations authorizes only that source change; it is not an Agent Sync invocation unless the Human separately invokes the declared Agent Sync entry point.

**Mode `3` (install).** Activate explicitly when the Human requests capability discovery, when a capability the Agent Module declares as Prepared or Installed is not present and usable in the Runtime, or when a required capability is absent from the synchronized Runtime. Never activate through another Skill, coordinator, automation, or model-generated action.

## Inputs

Accept exactly one required mode, given as a number: mode `1` (sync self) realizes only this Skill's own native adapter from the current Contract, and mode `2` (sync component) realizes every other Agent Module declaration. An invocation without a mode mutates nothing and reports all three modes together with whether the installed adapter still matches this Contract. Accept no capability selection in modes `1` and `2`. Consume the complete Agent Module, including its Agent Preferences, explicit empty categories, portable Skill Contracts, optional prepared Markdown Skill files matched by declared stable key, native project artifacts, and runtime-reported activation state. Obtain native paths, formats, mappings, and capability limits from the selected Agent Native's own documentation and runtime, rather than requiring them to be predeclared by the Module.

**Mode `3` (install).** Accept a requested capability need or derive needs from current Target technologies, frameworks, protocols, services, data sources, activities, Preferences, dependencies, and installed Agent capabilities. An empty explicit request performs complete relevant discovery from current evidence.

## Outputs

Produce one result for every dynamically discovered Agent Module declaration, reported as `synchronized`, `already synchronized`, `approximated`, `activation required`, `unmanaged`, or `blocked`, each naming the Module declaration it came from, the Native mechanism it was realized through, the exact project artifact that carries it, and the outcome of re-reading that artifact during verification, project-scoped native resources and additive provisioning authorized by selected declarations, post-change verification, preserved unmanaged capabilities, required Human activation steps, and one truthful overall Module status. An `approximated` result names the nearest Native mechanism used and states exactly how the realization differs from the declaration. A successful overall status certifies that every required declaration is currently realized and usable, and lists every approximation so the Human can judge it. A mode `1` run, a mode `2` run blocked by a stale adapter, or a mode-less invocation reports the resolved mode and its outcome, plus the declarations left unreconciled, instead of an overall Module status.

Record every mode `1` and mode `2` run in one project-scoped, machine-readable synchronization record: one entry per examined declaration naming its Module source, the source fingerprint it was realized from, its native artifact, its status, the resolved mode, and the time of the run, so a later run can prove idempotency and a non-Sync consumer can learn the last synchronized state without entering the Agent Module. The record's location and format are native details owned by the adapter.

Whenever the selected Native Runtime cannot apply a realized artifact change within the currently running instance — most commonly because it loads that artifact only at process or session start — give the required restart its own unmistakable notice in the report — visually set apart from surrounding text, in a box or equivalent — never folded only into a mapping-table row. A mode `1` run that rewrote its own adapter carries this same unmistakable notice, and a mode `2` run carries it whenever reconciliation wrote any native artifact, even when the overall Module status is otherwise a success.

**Mode `3` (install).** Produce an evidence-backed need inventory, candidate comparison, exact provisioning preview, approval request, and final status for every need as installed, updated, already available, activation required, not found, rejected, or blocked.

## Required Understanding

Agent Sync first establishes Interface Understanding, then understands the complete Agent Module without limiting the set of declarations it reads. It also understands the selected Agent Native from that Native's own documentation, structure, conventions, capabilities, and limitations. The Module supplies the portable meaning, principles, profiles, skills, rules, roles, context, and other declarations; the Native Runtime supplies the concrete places, formats, activation mechanisms, and runtime behavior used to realize them. Agent Sync places the Module's content into those Native places as the Human authored it, restating a declaration in the Native's idiom only where that makes the concept land better in the Native's own configuration and never where it would shift its scope, verifies the complete result, and leaves other Runtime operations dependent only on the synchronized realization. It never uses Target Understanding and never asks the Module to describe an unknown Native Runtime in advance.

Establish Interface Understanding, then read and understand the complete Agent Module through the sole exception that permits entry into its sources, beginning with the Agent Module Guide at `.interface/agent/guide.md`, which carries the Agent Structure. Discover all current Module declarations from that Agent Structure and current Module sources without a hardcoded component or category list. Learn the selected Agent Native's own documentation, supported capabilities, file conventions, mappings, invocation rules, and limitations before choosing any realization. No Target Understanding and no Understanding of any Interface Module other than the Agent Module is used or required. No other Skill, supporting Agent Instance, coordinator, or Understanding workflow may read, resolve, or use these Agent Module sources. Never rely on a list remembered by this Contract, a native adapter, or an earlier run.

**Mode `3` (install).** Establish Interface Understanding and Target Understanding. Read the complete Agent Module through the exception that permits entry into its sources, so every declared capability and its Capability Realization Kind is known. Read applicable Implementation Components, synchronized Runtime capability state, selected defaults, manifests, lockfiles, runtime versions, implementation evidence, and current capability status. Never modify an Agent Module source; a candidate that should become part of the portable Agent definition is reported for Human declaration rather than written here.

## Authority

Modify only project-scoped native Agent artifacts selected by the Native Runtime. Provision only exact Human-selected declarations. Never modify Interface sources or Config, Target code, application dependencies, credentials, user or machine settings, or unrelated Human work. The synchronization record is a project-scoped native artifact owned by this Skill; writing it is within this Authority and is neither an Interface source nor a Config write. Explicit Human invocation of this Skill's declared entry point is itself the standing authorization to create, rewrite, or reconcile any native artifact within this Authority; once invoked, do not pause the run to ask the Human whether to proceed with a write this Authority already permits. Only the exceptions named in Workflow Invariants and Stopping Conditions — credentials, external trust, broader scope, ambiguous ownership, destructive replacement of unrelated Human content, or an irreversible action — stop the run for Human action.

**Mode `3` (install).** Discovery is read-only. After explicit approval, transfer declared Prepared content and provision only named candidates at project scope through supported Agent capability mechanisms. Never change application dependencies, Target code, Interface sources, credentials, or user- or machine-scoped state.

## Workflow Invariants

**Modes `1` and `2` (Agent Sync):**

- Report the current phase to the Human as the run moves through it, not only in the final report.
- Announce entering Understanding, entering comparison of the Module against installed native artifacts, entering reconciliation that changes native configuration, and entering each Verification pass, including a repeated cycle.
- This narration runs throughout modes `1` and `2` alike and is never deferred until completion.
- When the selected Native Runtime caches a realized artifact at process or session start and cannot apply a rewritten artifact within the currently running instance, classify that artifact `activation required` with the Human action being an instance restart, and give that restart instruction its own unmistakable notice in the report rather than folding it only into a mapping-table row.
- This applies to a mode `1` run that rewrote its own adapter and to a mode `2` run that wrote any native artifact.
- Resolve the invoked mode before any mutation.
- In mode `1` (sync self), realize only this Skill's own native adapter from the current Contract and reconcile no other declaration.
- Realizing it means reading this Contract and the installed adapter in full, comparing them section by section, and rewriting the adapter whenever it instructs something this Contract no longer requires, omits something this Contract requires, or states a rule this Contract has changed.
- A mode `1` run whose comparison finds such a difference and leaves the adapter unwritten has not realized it, and reports itself as failed rather than unchanged.
- In mode `2` (sync component), first confirm the installed adapter still matches this Contract; when it does not, mutate nothing and block with the exact difference and the instruction to run mode `1` first, because the running instance never claims to have executed a definition it did not load.
- A mode `1` run never reports the complete Module as synchronized.
- Dynamically enumerate every current declaration and resource in the complete Agent Module before mutation.
- A Component, category, or supported mechanism added later is automatically part of the same run without requiring a hardcoded list change.
- Learn the selected Agent Native's realization mechanisms from its own documentation and runtime.
- Do not require a project-side `component_realization` map or predeclared native path, format, or capability mapping; if the Native cannot realize a required Module declaration exactly, realize it through the nearest Native mechanism, report it as approximated with the exact difference, and continue the run; report it as blocked only when no Native equivalent exists or a Stopping Condition applies.
- The run never stops because one declaration is approximated or blocked.
- When a declaration carries optional per-Agent-Native details, use only the block matching the selected Agent Native, treat it as an aid that narrows discovery rather than an authority that overrides the Native's own mechanism, ignore blocks declared for other Agent Natives, and fall back to the Native's own documentation when no matching block exists or the declared detail conflicts with the Native's actual mechanism.
- Never infer a native destination from a familiar directory layout.
- Realize every discovered Module declaration through the same explicit ordered procedure, one declaration at a time, with no declaration exempted and no shortcut permitted for one that looks current.
- For each declaration: read every source it owns in full; read the installed native artifact that realizes it in full; compare them section by section and record every difference of these three kinds, where the artifact instructs something the declaration no longer requires, omits something the declaration requires, or states a rule the declaration has changed; when any difference is recorded, rewrite the whole artifact so it carries what the declaration currently requires, keeping the metadata the Runtime needs and the native execution detail the declaration deliberately leaves to the artifact; re-read the written artifact and prove each recorded difference is gone, reporting as blocked any difference that survives; record the fingerprint of every source read for this declaration in the artifact's native metadata; and record the outcome as this declaration's mapping row naming the sources read, the artifact path, and what re-reading proved.
- Include empty and already-satisfied categories, and identify the Native mechanism and verification gate as part of the same pass.
- Claim no change or already synchronized for a declaration only from a comparison performed in this run against both files read in full.
- Presence of the artifact, its metadata fields, its modification time, its apparent recency, and the absence of a remembered edit are never evidence of conformance.
- A recorded source fingerprint follows Agent Skill Principles: a changed fingerprint proves staleness and requires reconciliation; an unchanged fingerprint never proves conformance.
- A run may consult recorded fingerprints to report provable staleness first; it never uses them to skip, defer, or shorten any declaration's procedure.
- A run that leaves any declaration unread, or that classifies one as unchanged without that recorded comparison, has not realized the Module: it fails verification and reports the unexamined declarations by name rather than reporting the Module as synchronized.
- Resolve ownership and classify each item as no change, create, update, install, enable, approximate, activation required, report only, or blocked.
- Never silently skip an unknown, new, or unsupported Component, category, or mechanism.
- Reconcile it when the selected Runtime supplies an authorized mapping; otherwise report it as blocked with the missing mapping or capability.
- Preserve compatible native values left unspecified and report undeclared capabilities as unmanaged unless they conflict; never remove them automatically.
- Verify Native Runtime compatibility first, derive dependency-safe reconciliation order from current Module relationships and Native capabilities, and preserve each declaration's ownership throughout execution.
- Reload or activate a changed capability when the selected Runtime supports doing so safely.
- Treat a selected desired state as standing authorization only for exact additive project-scoped reconciliation.
- Credentials, external trust, broader scope, destructive replacement, irreversible action, or missing authority still requires Human action.
- Rewriting or overwriting an existing native artifact that this Contract owns and that the current declaration authorizes is the ordinary reconciliation this Skill exists to perform, not the destructive replacement this bullet reserves for Human action; that reservation is for content whose ownership is ambiguous or that belongs to unrelated Human work.
- Do not ask the Human to confirm an ordinary reconciliation write already authorized by explicit invocation.
- Materialize the smallest self-contained native adapter that completely and faithfully realizes its portable Contract — the Contract's obligations carried as written, the Native's mechanics added around them — without requiring any later Agent Module read.
- Compare an existing adapter's own instruction content against its current Contract, not only its presence or its declared metadata fields.
- When the Contract no longer matches what the adapter instructs, regenerate that adapter's content rather than classifying it as no change.
- Runtime references may point to other synchronized Runtime artifacts, but never to Agent Module sources.
- Never invent content for an empty category.
- Realize only Constructed Skills: an Interface-owned Skill defined by a portable Contract is built from that Contract into a self-contained native Skill.
- A Prepared Skill and an Installed Skill are outside the sync modes; mode `3` (install) of this same Skill owns them.
- Treat Agent Module changes as dormant desired state until this explicit synchronization completes.
- Never trigger synchronization from another Skill, startup routine, or ordinary Interface Understanding.
- Reconcile every Runtime instruction that could route a non-Sync consumer into the Agent Module.
- Replace such routing with the corresponding synchronized Runtime Rule, capability, Agent Instance, or Skill realization.
- Write only to a project-scoped destination that the Agent Native documents for the realized declaration and that its owning Module declaration authorizes.
- A Native-provided or explicitly unused declaration is observation-only.
- Explicitly unused means no capability is required; it never authorizes removal of an observed undeclared capability.
- Preserve meaningful Human-authored runtime content when ownership is ambiguous and report the exact conflict.

**Mode `3` (install):**

- Resolve every declared capability's Capability Realization Kind.
- A Prepared capability is transferred into the selected Runtime unchanged, preserving every file of its source tree and its internal relative paths, adapting only the native metadata required for discovery.
- An Installed capability is provisioned through the native mechanism its owning provider declaration names.
- A Constructed capability is never materialized here; it belongs to Agent Sync.
- Match a declared name against the capability's own name within a Runtime's namespaced identifier rather than requiring an exact string match, so an already-present capability is recognized instead of provisioned again.
- Treat capability as covering Skills, plugins, MCP servers, and every other provider-supplied Agent capability the selected Runtime supports.
- After the project's packages are installed, use the skill-provisioning mechanism the applicable Language Item declares when one exists, so capabilities bundled by installed packages become discoverable.
- The absence of a declaration never means no mechanism exists, and a declared mechanism never replaces the environment's own current capability.
- Enumerate distinct capability needs with exact evidence before search.
- Check current availability before discovery and search every relevant route supported by the active Runtime.
- Verify candidate purpose, source, included components, permissions, dependencies, project scope, and version compatibility.
- Prefer an official source, then the technology maintainer, then a trusted third party.
- Reject duplicates and candidates without supported project scope.
- State the routes checked for a negative result.
- Adding a marketplace, trusting or connecting a service, or changing an installation source is provisioning and requires approval.
- Preview one result for every identified need and ask approval for exact candidates before any mutation.
- Verify post-install discovery, enablement, connection, expected capabilities, and usability.
- File presence or an installation receipt is insufficient.

## Verification

- After reconciliation, discard the pre-change observations and perform a second complete pass from the canonical Agent Structure and complete Agent Module.
- Re-read every discovered Module source and native artifact, query current runtime state, and prove every Module declaration and mechanism is realized and usable, including the active Agent Native, instantiable Agent Instance Definitions, correct Role and capability assignments, discoverable self-contained Skills whose native invocation controls match their declared Human and coordinator Invocation Policies and whose instruction content currently reflects their portable Contract, resolvable Commands, matching effective settings and enforcement, active selected Extensions, usable selected Integrations, and absence of secrets in project artifacts.
- Audit all synchronized non-Sync instructions and mappings and fail verification if any of them directs its consumer to read, resolve, or use an Agent Module source.
- For every enforced guarantee the Permission Preferences declare, run at least one behavioral probe — an action that the guarantee must block or permit, defined for the selected Agent Native beside the guarantee — and record whether the observed behavior matched; a guarantee whose probe fails is not realized, whatever its artifacts say.
- Probes are the evidence for the third success condition: that the Agent behaves as declared, not only that its artifacts exist.

- Report this second pass as one mapping record per declaration, stating what the Module declared, what it was realized as, where that realization lives, whether re-reading it proved conformance, and, for an enforced guarantee, what its behavioral probe observed.
- A record claims conformance only from evidence re-read in this pass; a write that succeeded is not itself conformance, and a record without a named artifact is not a claim.

- The overall result is `synchronized` only when this second pass covers the complete current Agent Module and every required item passes its own verification gate.
- An approximated item passes its gate when re-reading proves the nearest realization is in place and its stated difference is still accurate.
- Any blocked, missing, conflicting, inactive, unsupported, or unverified required item prevents the success claim, even when all other declarations pass.

- When this pass finds a required item unrealized, incompletely realized, or unverified for a reason other than a genuine Stopping Condition, do not stop at reporting it.
- Return to Understanding, reconcile that item again under the current Module and Native state, and perform a new complete Verification pass.
- Repeat this Understanding-Reconcile-Verify cycle within the same invocation until every required item either passes its verification gate or is reported as blocked under a genuine Stopping Condition.
- Stop repeating only when a cycle changes nothing from the previous cycle's outcome — the same items realized, the same items blocked for the same reason — or when every required item is realized and verified.
- A cycle that only reproduces its own last outcome has converged, not stalled, and is reported as the final result rather than repeated again.

- **Mode `3` (install).** Prove the installed capability is project-declared, active, discoverable, and usable by its intended Role.
- Report pending authentication, trust, reload, restart, or external activation instead of success.

## Idempotency

After successful reconciliation, a new invocation against unchanged declarations and runtime state produces no mutation. A newly added or changed Agent Module declaration, Principle, Preferences, Contract, resource, category, or mechanism is detected from current sources and reconciled on the next invocation.

**Mode `3` (install).** Against unchanged evidence and releases, preserve adequate capabilities and perform no duplicate provisioning.

## Stopping Conditions

- Block an affected item on incompatible Runtime, ambiguous ownership, unsupported project scope, destructive conflict, missing provider, or unavailable authority.
- Mark pending restart, authentication, or trust as activation required.
- Independent items continue when dependencies permit.
- Stop a mode `2` run before any mutation when the installed adapter no longer matches this Contract, and report that a mode `1` run is required first.

- **Mode `3` (install).** Stop before provisioning without explicit candidate approval.
- Block candidates that are incompatible, untrusted, duplicate, unavailable at project scope, or require unauthorized access.
- Pause for Human trust, authentication, or another external activation step.

## Runtime Realization

The native `agent-native` adapter is the only Runtime artifact that may bootstrap from this Contract and the complete Agent Module. It first establishes Native Runtime Understanding from the selected Agent Native's own documentation and runtime, then realizes its own adapter from the current Contract in mode `1` (sync self), and in mode `2` (sync component) dynamically traverses the Agent Module and realizes it through native mechanisms without an exhaustive component or mechanism list. Every other native Skill and Agent Instance must be self-contained or depend only on synchronized Runtime artifacts and must never resolve its behavior through an Agent Module source. The adapter cannot depend on the previous presence of another vendor's adapter. It reports its current phase to the Human through the Native's own output as it moves through Understanding, comparison, reconciliation, and each Verification pass, and repeats the Understanding-Reconcile-Verify cycle within the same invocation until the run converges, rather than stopping at the first Verification pass that finds a resolvable gap. The adapter may own a bounded fingerprint helper that hashes sources, records fingerprints in native metadata, and reads or writes the synchronization record; it never compares instruction content and never decides conformance.

**Mode `3` (install).** A native adapter discovers current provider commands and catalogs through Runtime mappings rather than hardcoding vendors, and presents both the need inventory and candidate-result inventory before installation.

# agent-sync Skill Contract

## Purpose

Reconstruct the complete Agent Module and realize it in the compatible project-scoped Agent Runtime.

## Responsibility

Establish Interface Understanding, understand the complete Agent Module, learn the selected Agent Native's own documented capabilities and conventions, realize this Skill's own adapter in `self` mode and every other declaration in `module` mode, translating the Module into that Native Runtime under the invoked mode. Reconcile authorized project artifacts and already-selected capabilities and prove complete availability. Agent Sync applies existing Human choices; it never discovers or selects new ones. Report an undeclared need for Human declaration and the separate Skill Installer operation instead of adopting it here.

## Trigger

Activate only when the Human directly invokes the declared Runtime entry point while setting up, repairing, migrating, updating, or auditing an Agent Runtime. The Agent Native, every Agent Instance, Skill, coordinator, Hook, startup or resume routine, automation, and model-generated action are forbidden from invoking, chaining, triggering, or simulating this Skill. A Human request to change Agent Module declarations authorizes only that source change; it is not an Agent Sync invocation unless the Human separately invokes the declared Agent Sync entry point.

## Inputs

Accept exactly one required semantic mode: `self` realizes only this Skill's own native adapter from the current Contract, and `module` realizes every other Agent Module declaration. An invocation without a mode mutates nothing and reports both modes together with whether the installed adapter still matches this Contract. Accept no capability selection. Consume the complete Agent Module, including its Agent Profile, explicit empty categories, portable Skill Contracts, optional prepared Markdown Skill files matched by declared stable key, native project artifacts, and runtime-reported activation state. Obtain native paths, formats, mappings, and capability limits from the selected Agent Native's own documentation and runtime, rather than requiring them to be predeclared by the Module.

## Outputs

Produce one result for every dynamically discovered Agent Module declaration, reported as `synchronized`, `already synchronized`, `activation required`, `unmanaged`, or `blocked`, project-scoped native resources and additive provisioning authorized by selected declarations, post-change verification, preserved unmanaged capabilities, required Human activation steps, and one truthful overall Module status. A successful overall status certifies that every required declaration is currently realized and usable. A `self` run, a `module` run blocked by a stale adapter, or a mode-less invocation reports the resolved mode and its outcome, plus the declarations left unreconciled, instead of an overall Module status.

## Understanding

Agent Sync first establishes Interface Understanding, then understands the complete Agent Module without limiting the set of declarations it reads. It also understands the selected Agent Native from that Native's own documentation, structure, conventions, capabilities, and limitations. The Module supplies the portable meaning, principles, profiles, skills, rules, roles, context, and other declarations; the Native Runtime supplies the concrete places, formats, activation mechanisms, and runtime behavior used to realize them. Agent Sync translates between these two sides, verifies the complete result, and leaves other Runtime operations dependent only on the synchronized realization. It never uses Target Understanding and never asks the Module to describe an unknown Native Runtime in advance.

## Required Understanding

Establish Interface Understanding, then read and understand the complete Agent Module through the sole exception that permits entry into its sources. Discover all current Module declarations from the Agent Structure and current Module sources without a hardcoded component or category list. Learn the selected Agent Native's own documentation, supported capabilities, file conventions, mappings, invocation rules, and limitations before choosing any realization. No Target Understanding and no Understanding of any Interface Module other than the Agent Module is used or required. No other Skill, supporting Agent Instance, coordinator, or Understanding workflow may read, resolve, or use these Agent Module sources. Never rely on a list remembered by this Contract, a native adapter, or an earlier run.

## Authority

Modify only project-scoped native Agent artifacts selected by the Native Runtime. Provision only exact Human-selected declarations. Never modify Interface sources or Config, Target code, application dependencies, credentials, user or machine settings, or unrelated Human work.

## Workflow Invariants

- Resolve the invoked mode before any mutation. In `self` mode, realize only this Skill's own native adapter from the current Contract and reconcile no other declaration. In `module` mode, first confirm the installed adapter still matches this Contract; when it does not, mutate nothing and block with the exact difference and the instruction to run `self` first, because the running instance never claims to have executed a definition it did not load. A `self` run never reports the complete Module as synchronized.
- Dynamically enumerate every current declaration and resource in the complete Agent Module before mutation. A Component, category, or supported mechanism added later is automatically part of the same run without requiring a hardcoded list change.
- Learn the selected Agent Native's realization mechanisms from its own documentation and runtime. Do not require a project-side `component_realization` map or predeclared native path, format, or capability mapping; if the Native cannot realize a required Module declaration, report the exact unsupported or ambiguous item as blocked. When a declaration carries optional per-Agent-Native details, use only the block matching the selected Agent Native, treat it as an aid that narrows discovery rather than an authority that overrides the Native's own mechanism, ignore blocks declared for other Agent Natives, and fall back to the Native's own documentation when no matching block exists or the declared detail conflicts with the Native's actual mechanism. Never infer a native destination from a familiar directory layout.
- For every discovered Module declaration, read all sources it owns, derive its complete desired state, identify the Native mechanism that realizes it, observe actual state, and record the proposed action and verification gate. Include empty and already-satisfied categories.
- Resolve ownership and classify each item as no change, create, update, install, enable, activation required, report only, or blocked.
- Never silently skip an unknown, new, or unsupported Component, category, or mechanism. Reconcile it when the selected Runtime supplies an authorized mapping; otherwise report it as blocked with the missing mapping or capability.
- Preserve compatible native values left unspecified and report undeclared capabilities as unmanaged unless they conflict; never remove them automatically.
- Verify Native Runtime compatibility first, derive dependency-safe reconciliation order from current Module relationships and Native capabilities, and preserve each declaration's ownership throughout execution. Reload or activate a changed capability when the selected Runtime supports doing so safely.
- Treat a selected desired state as standing authorization only for exact additive project-scoped reconciliation. Credentials, external trust, broader scope, destructive replacement, irreversible action, or missing authority still requires Human action.
- Materialize the smallest self-contained native adapter that completely realizes its portable Contract without requiring any later Agent Module read. Compare an existing adapter's own instruction content against its current Contract, not only its presence or its declared metadata fields. When the Contract no longer matches what the adapter instructs, regenerate that adapter's content rather than classifying it as no change. Runtime references may point to other synchronized Runtime artifacts, but never to Agent Module sources. Never invent content for an empty category.
- Realize only Constructed Skills: an Interface-owned Skill defined by a portable Contract is built from that Contract into a self-contained native Skill. A Prepared Skill and an Installed Skill are outside this operation; the Skill Installer operation owns them.
- Treat Agent Module changes as dormant desired state until this explicit synchronization completes. Never trigger synchronization from another Skill, startup routine, or ordinary Interface Understanding.
- Reconcile every Runtime instruction that could route a non-Sync consumer into the Agent Module. Replace such routing with the corresponding synchronized Runtime Rule, capability, Agent Instance, or Skill realization.
- Write only to a project-scoped destination that the Agent Native documents for the realized declaration and that its owning Module declaration authorizes. A Native-provided or explicitly unused declaration is observation-only. Explicitly unused means no capability is required; it never authorizes removal of an observed undeclared capability.
- Preserve meaningful Human-authored runtime content when ownership is ambiguous and report the exact conflict.

## Verification

After reconciliation, discard the pre-change observations and perform a second complete pass from the canonical Agent Structure and complete Agent Module. Re-read every discovered Module source and native artifact, query current runtime state, and prove every Module declaration and mechanism is realized and usable, including the active Agent Native, instantiable Agent Instance Definitions, correct Role and capability assignments, discoverable self-contained Skills whose native invocation controls match their declared Human and coordinator Invocation Policies and whose instruction content currently reflects their portable Contract, resolvable Commands, matching effective settings and enforcement, active selected Extensions, usable selected Integrations, and absence of secrets in project artifacts. Audit all synchronized non-Sync instructions and mappings and fail verification if any of them directs its consumer to read, resolve, or use an Agent Module source.

The overall result is `synchronized` only when this second pass covers the complete current Agent Module and every required item passes its own verification gate. Any blocked, missing, conflicting, inactive, unsupported, or unverified required item prevents the success claim, even when all other declarations pass.

## Idempotency

After successful reconciliation, a new invocation against unchanged declarations and runtime state produces no mutation. A newly added or changed Agent Module declaration, Principle, Profile, Contract, resource, category, or mechanism is detected from current sources and reconciled on the next invocation.

## Stopping Conditions

Block an affected item on incompatible Runtime, ambiguous ownership, unsupported project scope, destructive conflict, missing provider, or unavailable authority. Mark pending restart, authentication, or trust as activation required. Independent items continue when dependencies permit. Stop a `module` run before any mutation when the installed adapter no longer matches this Contract, and report that a `self` run is required first.

## Runtime Realization

The native `agent-sync` adapter is the only Runtime artifact that may bootstrap from this Contract and the complete Agent Module. It first establishes Native Runtime Understanding from the selected Agent Native's own documentation and runtime, then realizes its own adapter from the current Contract in `self` mode, and in `module` mode dynamically traverses the Agent Module and realizes it through native mechanisms without an exhaustive component or mechanism list. Every other native Skill and Agent Instance must be self-contained or depend only on synchronized Runtime artifacts and must never resolve its behavior through an Agent Module source. The adapter cannot depend on the previous presence of another vendor's adapter.

# Agent Skill Principles

Agent Skill is the Component that defines the architecture-level requirements for reusable knowledge or workflows an Agent Role can activate. Portable Skill Contract resources define each Interface-owned Skill completely, and runtime implementations translate those contracts into focused, discoverable instructions. Externally provided Skills remain provider-owned capabilities declared by the Agent Profile.

It owns Skill contracts and activation boundaries. It does not own the project facts, Component policies, or runtime tools it consumes.

## Terms

- **Skill** — reusable instructions or knowledge activated explicitly or by relevance.
- **Skill Contract** — the portable definition of an Interface-owned Skill's responsibility, inputs, outputs, authority, checks, and stopping conditions.
- **Activation** — the state in which a Skill is discoverable and usable by its intended role.

## Relationships

- **Consumes Agent Role, Context, Rule, Tool, and Permission** — executes within their contracts.
- **Consumes Developer Components and Target** — reads current authorities required by its responsibility.
- **Consumed by Agent Command and Coordination** — provides invocable and delegable workflows.

Each Interface-owned Skill's portable behavior belongs to its Skill Contract under the Agent Skill Component. Technical Skill catalogs, external provider Skills, activation choices, provider resources, and native implementation mappings belong to Agent Skill Preferences. Command names and argument forms belong to Agent Command Preferences.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every Skill has one complete contract

**Rule:** Every Interface-owned Skill has exactly one portable Skill Contract, conforming to the Skill Contract Schema, that declares its purpose, responsibility, trigger, inputs, outputs, required Understanding, authority, workflow invariants, verification, idempotency expectation, stopping conditions, and runtime-realization requirements. Principles own rules shared by Skills, the Skill Contract owns Skill-specific behavior independent of a runtime, and a native Skill implementation owns only runtime-specific execution details and never overrides or becomes a second authority for its Contract.

**Why:** A Skill must remain focused and current when project definitions change.

**Boundary:** A coordinating Skill Contract may require an exact orchestration sequence when orchestration is its single declared responsibility. An external Skill, including framework and package-provided Skills, remains governed by its provider resource, Profile declaration, applicable Agent Principles, and the active Role; it does not receive an Interface-owned Skill Contract.

<br>

## 2. Skill availability is proven

**Rule:** A Skill is available only when its intended Agent Role can discover and invoke it in the current project. A file, installation record, or declaration alone does not prove Activation.

**Why:** Planning around nominal Skills fails when the runtime cannot actually load them.

**Boundary:** Validation may report the unmet activation condition without changing it.

<br>

## 3. Skill execution is safely repeatable

**Rule:** Repeating a Skill against unchanged authorities and state preserves valid work and produces no unnecessary mutation. A Skill reconciles current evidence rather than regenerating blindly.

**Why:** Skills are routinely resumed and rerun across sessions.

**Boundary:** Repeatability never authorizes destructive replacement of meaningful work.

<br>

## 4. `configure` establishes operational readiness

**Rule:** The architecture requires the `configure` Skill. Its purpose is operational readiness; its responsibility is to initialize and reconcile Config, synchronize stable phase identity and aggregate State, and prepare the selected Environment; its task coverage is configuration and environment preparation required before workflow execution.

**Why:** Every later operation needs valid operational records and a prepared execution environment.

**Boundary:** `configure` never stores Target meaning, plans, develops, reviews, launches, resets, or modifies non-Config Interface sources.

<br>

## 5. `planning` owns work definition

**Rule:** The architecture requires the `planning` Skill. Its purpose is executable work definition; its responsibility is to convert current Target Understanding and applicable Component authorities into complete, bounded, ordered, and verifiable Tasks for selected or all eligible phases; its task coverage is decomposition, dependencies, acceptance, verification conditions, and Plan reconciliation.

**Why:** Development needs an explicit statement of what must be achieved and how completion will be observed.

**Boundary:** `planning` never prescribes implementation, performs development, reviews results, or changes Target intent.

<br>

## 6. `developing` owns implementation and its checks

**Rule:** The architecture requires the `developing` Skill. Its purpose is verified implementation; its responsibility is to execute eligible planned work, resolve implementation details within current authorities, build durable checks from Task verification conditions, and record truthful evidence; its task coverage is selected or all eligible planned phase work.

**Why:** Planned outcomes become trustworthy only through implementation and observable verification.

**Boundary:** `developing` never creates the Plan, performs independent Review, changes Target intent, or writes outside Development authority.

<br>

## 7. `reviewing` independently judges results

**Rule:** The architecture requires the `reviewing` Skill. Its purpose is independent assurance; its responsibility is to judge implemented results against current Target Understanding, Component authorities, Plans, acceptance criteria, and observable evidence; its task coverage is verification, Findings, evidence gaps, and exact Review outcomes.

**Why:** The operation that produced a result cannot provide fully independent judgment of that result.

**Boundary:** `reviewing` reports and records; it never repairs implementation, replans work, invents requirements, or changes another operation's progress.

<br>

## 8. `launch` owns runtime startup and readiness

**Rule:** The architecture requires the `launch` Skill. Its purpose is operational availability; its responsibility is to verify the selected Environment, start completed Target parts through declared public boundaries, verify readiness, and report Access Points; its task coverage is runtime startup, dependency order, readiness, and access reporting.

**Why:** Completed implementation is not operational until startup and readiness are observed.

**Boundary:** `launch` never prepares the Environment, repairs product code, changes Target intent, or bypasses incomplete prerequisites.

<br>

## 9. `implement` is the trustworthy full-path coordinator

**Rule:** The architecture requires the `implement` Skill. Its purpose is trustworthy end-to-end execution; its responsibility is to coordinate Configure, baseline Review where prior work exists, Planning, Development, independent final Review, Finding reconciliation, and eligible Launch while preserving each Skill's authority; its task coverage is selected phases or all implementable phases.

**Why:** A single entry point is needed when the Human wants a complete evidence-backed implementation rather than manual operation-by-operation control.

**Boundary:** `implement` coordinates and integrates outcomes; it performs no product operation of its own and never bypasses an operation gate or Human approval.

<br>

## 10. `reset` owns previewed workflow rollback

**Rule:** The architecture requires the `reset` Skill. Its purpose is controlled workflow rollback; its responsibility is to resolve and preview one declared reset stage, obtain explicit Human confirmation, and apply only that preview; its task coverage is the exact operational and implementation outputs owned by the selected stage.

**Why:** Destructive workflow rollback needs one controlled and auditable entry point.

**Boundary:** `reset` never treats invocation as approval, removes an unlisted target, interprets Target intent, reverses Environment preparation, or invokes another workflow operation afterward.

<br>

## 11. `skill-installer` owns Agent capability provisioning

**Rule:** The architecture requires the `skill-installer` Skill. Its purpose is controlled Agent capability lifecycle management; its responsibility is to derive needs, discover compatible project-scoped candidates, preview provenance, permissions, dependencies, and scope, obtain approval, provision approved choices, and verify Activation; its task coverage is Agent capabilities rather than application dependencies.

**Why:** Agent capabilities need a controlled lifecycle distinct from application dependency installation.

**Boundary:** `skill-installer` never changes Target code or dependencies, installs at user scope, stores credentials, provisions before approval, or treats discovery as Activation.

<br>

## 12. `fastapi` supplies conditional FastAPI guidance

**Rule:** The current Agent Profile requires the `fastapi` contextual Skill only when FastAPI work is selected by a current authority. Its purpose is current framework guidance; its responsibility is to supply reusable FastAPI knowledge inside the active role; its task coverage is APIs, validation, dependencies, responses, routing, streaming, and related implementation concerns.

**Why:** Technology-specific work benefits from focused current knowledge without coupling the Agent architecture to one Target.

**Boundary:** `fastapi` provides guidance inside the active role; it never selects FastAPI, expands project scope, overrides Developer or Target authorities, or becomes a workflow operation.

<br>

## 13. `typer` supplies conditional Typer guidance

**Rule:** The current Agent Profile requires the `typer` contextual Skill only when Typer work is selected by a current authority. Its purpose is current CLI-framework guidance; its responsibility is to supply reusable Typer knowledge inside the active role; its task coverage is applications, commands, arguments, options, output, and related implementation concerns.

**Why:** CLI-specific knowledge should be available when relevant without becoming a universal Target requirement.

**Boundary:** `typer` provides guidance inside the active role; it never selects Typer, expands project scope, overrides Developer or Target authorities, or becomes a workflow operation.

<br>

## 14. `library-skills` conditionally manages package-provided Skills

**Rule:** The current Agent Profile requires the `library-skills` contextual Skill only when installed project packages may provide Agent Skills or managed links need reconciliation. Its purpose is package-provided Skill lifecycle management; its responsibility is to preserve and reconcile package-owned Skill links; its task coverage is discovery, installation, update, repair, and status checks for those Skills.

**Why:** Package-owned Agent guidance needs lifecycle management that preserves its provenance and does not overwrite hand-authored Skills.

**Boundary:** `library-skills` never substitutes for general capability discovery, changes application dependencies as an Agent capability action, deletes hand-authored Skills, or expands beyond package-provided Skill management.

<br>

## 15. `agent-sync` realizes the declared Agent Profile

**Rule:** The architecture requires the `agent-sync` Skill. Its purpose is portable Agent Profile realization; its responsibility is to compare every Agent Component's Human-owned declarations with the selected Runtime, reconcile authorized project-scoped native artifacts and selected capabilities, and verify actual availability; its task coverage is the complete Agent Profile, including explicit empty categories.

**Why:** A portable Agent definition is useful only when a compatible Runtime can reconstruct and prove the same operational Agent without repeated manual setup.

**Boundary:** `agent-sync` never changes Interface sources, Target code, application dependencies, user- or machine-scoped state, credentials, or Human choices; it never discovers or adopts undeclared capabilities, removes compatible unmanaged capabilities, or treats declaration or file presence as proof of Activation.

<br>

## At a Glance

- **Must** — give every Interface-owned Skill exactly one complete portable Contract conforming to the Skill Contract Schema *(1)*
- **Must** — keep shared rules in Principles, Skill-specific behavior in its Contract, and runtime execution details in the native implementation *(1)*
- **Never** — let a native Skill implementation override or become a second authority for its Contract *(1)*
- **Must** — prove Skill availability through discovery and invocation *(2)*
- **Must** — make repeated execution preserve valid work *(3)*
- **Never** — use repeatability to justify destructive regeneration *(3)*
- **Must** — provide `configure` for Config reconciliation, phase synchronization, and Environment preparation *(4)*
- **Never** — let `configure` perform another operation or modify non-Config Interface sources *(4)*
- **Must** — provide `planning` for complete, bounded, and verifiable work definition *(5)*
- **Never** — let `planning` prescribe implementation or perform downstream operations *(5)*
- **Must** — provide `developing` for implementation, durable checks, and truthful evidence *(6)*
- **Never** — let `developing` plan, independently review, or exceed Development authority *(6)*
- **Must** — provide `reviewing` for independent evidence-based judgment and Findings *(7)*
- **Never** — let `reviewing` repair, replan, invent requirements, or change another operation's progress *(7)*
- **Must** — provide `launch` for startup, readiness verification, and Access Points *(8)*
- **Never** — let `launch` prepare the Environment, repair code, or bypass prerequisites *(8)*
- **Must** — provide `implement` as the gated full-path coordinator *(9)*
- **Never** — let `implement` absorb operation authority or bypass a gate or approval *(9)*
- **Must** — provide `reset` for previewed and explicitly confirmed workflow rollback *(10)*
- **Never** — let `reset` infer approval or affect a target absent from its preview *(10)*
- **Must** — provide `skill-installer` for approved project-scoped Agent capability provisioning *(11)*
- **Never** — let `skill-installer` modify application dependencies, use user scope, or provision before approval *(11)*
- **Must** — activate `fastapi` only when current authorities select FastAPI work *(12)*
- **Never** — let `fastapi` select technology, change scope, or override authorities *(12)*
- **Must** — activate `typer` only when current authorities select Typer work *(13)*
- **Never** — let `typer` select technology, change scope, or override authorities *(13)*
- **Must** — activate `library-skills` only for package-provided Skill management *(14)*
- **Never** — let `library-skills` overwrite hand-authored Skills or replace general capability management *(14)*
- **Must** — provide `agent-sync` to reconcile and verify the complete declared Agent Profile at project scope *(15)*
- **Never** — let `agent-sync` change Human-owned declarations, Target code, broader-scope state, or adopt undeclared capabilities *(15)*

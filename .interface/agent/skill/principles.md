# Agent Skill Principles

Agent Skill is the Component that defines the architecture-level requirements for reusable knowledge or workflows an Agent Role can activate. Portable Skill Contract resources define each Interface-owned Skill completely, and runtime implementations translate those contracts into focused, discoverable instructions. Externally provided Skills remain provider-owned capabilities declared by the Agent Profile.

It owns Skill contracts and activation boundaries. It does not own the project facts, Component policies, or runtime tools it consumes.

## Terms

- **Skill** — reusable instructions or knowledge activated explicitly or by relevance.
- **Skill Contract** — the portable definition of an Interface-owned Skill's responsibility, inputs, outputs, authority, checks, and stopping conditions.
- **Prepared Skill File** — an optional Human-authored Markdown instruction body for one declared Skill, materialized by Agent Sync into that Skill's native Runtime folder without changing its meaning.
- **Activation** — the state in which a Skill is discoverable and usable by its intended role.
- **Invocation Policy** — whether a Skill may be invoked by the Human, by a declared coordinating Skill, or by both in the selected Runtime.

## Relationships

- **Consumes Agent Role, Context, Rule, Tool, and Permission** — executes within their contracts.
- **Consumes Implementation Components and Target** — reads current authorities required by its responsibility.
- **Consumed by Agent, Command, and Coordination** — provides assignable, invocable, and delegable workflows.

Each Interface-owned Skill's portable behavior belongs to its Skill Contract under the Agent Skill Component. Technical Skill catalogs, external provider Skills, activation choices, provider resources, and native implementation mappings belong to Agent Skill Profile. Command names and argument forms belong to Agent Command Profile.

Every statement here is mandatory. A Profile can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every Skill has one complete contract

**Rule:** Every Interface-owned Skill has exactly one portable Skill Contract, conforming to the Skill Contract Schema, that declares its purpose, responsibility, trigger, inputs, outputs, required Understanding, authority, workflow invariants, verification, idempotency expectation, stopping conditions, and runtime-realization requirements. Principles own rules shared by Skills, the Skill Contract owns Skill-specific behavior independent of a runtime, and a native Skill implementation is a synchronized, self-contained realization that owns only runtime-specific execution details and never overrides or becomes a second authority for its Contract.

**Why:** A Skill must remain focused and current when project definitions change.

**Boundary:** Only `agent-sync` reads the portable Contract inside the Agent Module. Every other Interface-owned Skill consumes its synchronized native realization without reading or resolving any Agent Module source. A coordinating Skill Contract may require an exact orchestration sequence when orchestration is its single declared responsibility. An external Skill, including framework and package-provided Skills, remains governed by its synchronized runtime realization and the active Role; it does not receive an Interface-owned Skill Contract.

<br>

## 2. Skill availability is proven

**Rule:** A Skill is available only when its intended Agent Role can discover and invoke it in the current project. A Skill delegated by another Skill is available only when the selected Runtime permits that declared coordinator to invoke it. Core Workflow Skills used by Implement are invocable both directly by the Human and by declared coordinators; top-level or sensitive coordinating Skills remain explicit-Human entry points unless the Skill Profile states otherwise. A file, installation record, or declaration alone does not prove Activation.

**Why:** Planning around nominal Skills fails when the runtime cannot actually load them.

**Boundary:** Coordinator invocation never expands the delegated Skill's scope, authority, permission requirements, or stopping conditions. Being coordinator-invocable does not authorize unrelated automatic execution. Validation reports an unmet invocation condition before a coordinating workflow mutates state.

<br>

## 3. Skill execution is safely repeatable

**Rule:** Repeating a Skill against unchanged authorities and state preserves valid work and produces no unnecessary mutation. A Skill reconciles current evidence rather than regenerating blindly.

**Why:** Skills are routinely resumed and rerun across sessions.

**Boundary:** Repeatability never authorizes destructive replacement of meaningful work.

<br>

## Skill-specific behavior

Each Skill's purpose, responsibility, workflow, inputs, outputs, authority, verification, idempotency, stopping conditions, and runtime realization belong only in its own portable Contract. This Principles file defines no Skill-specific workflow or implementation details.

<br>

## 4. A prepared Markdown file may supply a Skill's native instruction body

**Rule:** The Agent Skill Profile declares one optional prepared-file directory and an exact filename convention keyed by declared Skill identity. When the matching Markdown file exists, Agent Sync creates the Skill folder and entrypoint required by the selected Agent Native, preserves that file's instruction content and meaning, and adds or adapts only the minimum native metadata needed for discovery and invocation. When no matching file exists, Agent Sync realizes the Skill from its portable Contract, provider declaration, and Runtime mapping exactly as before.

**Why:** A complete Human-authored Skill should be reusable without forcing every Skill to have a prepared file or turning Runtime output into its source.

**Boundary:** File presence never declares a new Skill, selects a provider, proves Activation, or authorizes an unmatched file to be installed. A prepared file must match exactly one Skill already declared by the Profile and must conform to that Skill's Contract and applicable Principles. Only Agent Sync reads it; ordinary Runtime Skills consume the synchronized native copy. Agent Sync never rewrites the Human-owned source file or silently changes its semantic instructions.

<br>

## At a Glance

- **Must** — give every Interface-owned Skill exactly one complete portable Contract conforming to the Skill Contract Schema *(1)*
- **Must** — keep shared rules in Principles, Skill-specific behavior in its Contract, and runtime execution details in the native implementation *(1)*
- **Must** — make every non-Sync native Skill self-contained so it never resolves a Contract or capability through the Agent Module *(1, 15)*
- **Never** — let a native Skill implementation override or become a second authority for its Contract *(1)*
- **Must** — prove Skill availability through discovery and invocation *(2)*
- **Must** — make every delegated Skill invocable by its declared coordinator and verify the complete invocation chain before orchestration mutates state *(2)*
- **Never** — let coordinator invocation expand a delegated Skill's authority or permit unrelated automatic execution *(2)*
- **Must** — make repeated execution preserve valid work *(3)*
- **Never** — use repeatability to justify destructive regeneration *(3)*
- **Must** — materialize an exact matching prepared Skill file into the selected Agent Native's required Skill folder while preserving its instruction meaning *(4)*
- **Must** — keep the existing Contract- or provider-based realization path when a declared Skill has no prepared file *(4)*
- **Never** — infer a Skill from an unmatched file, treat a file as proof of Activation, or rewrite the Human-owned prepared source *(4)*

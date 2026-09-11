# Agent Observability Principles

Agent Observability is the Component that makes Agent configuration, execution, capability health, evidence, and outcomes inspectable. It defines diagnostics, status, logs, usage signals, and completion evidence without becoming the authority for the work observed.

It owns observation contracts and health vocabulary. It does not own implementation, project intent, hidden reasoning, or the records maintained by other Components.

## Terms

- **Observation** — a current, attributable fact obtained from an inspectable source or check.
- **Evidence** — an Observation sufficient to support a stated condition or outcome.
- **Capability Status** — the current availability classification of a declared capability.

## Relationships

- **Consumes every Agent Component** — evaluates their declarations and runtime realization.
- **Consumed by Agent Role, Interaction, and Session** — supplies diagnostics and evidence-backed outcome claims.

Technical checks, statuses, diagnostics, telemetry, logging, and usage reporting belong to Agent Observability Preferences.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Completion is evidence-backed

**Rule:** An Agent reports success only when every requested and contract-required condition has current observable Evidence. Missing or inconclusive Evidence remains explicit and never becomes success by inference.

**Why:** Stable outcomes require repeatable gates rather than confidence or plausible artifacts.

**Boundary:** Evidence proportional to risk is sufficient; redundant checks that cannot increase confidence are unnecessary.

<br>

## 2. Material execution is observable

**Rule:** Active scope, material decisions, mutations, delegation, checks, outcomes, blockers, configuration drift, Capability Status, and required Human actions are attributable and inspectable.

**Why:** Later Humans and Agents need to distinguish current fact from assumption and unfinished work.

**Boundary:** Hidden reasoning, secrets, and irrelevant command transcripts are never observability requirements.

<br>

## 3. Health claims use controlled status vocabulary

**Rule:** Capability and configuration health use declared statuses with objective entry conditions. A status changes only when current Observation establishes the new condition.

**Why:** Stable vocabulary makes diagnostics comparable across runtimes and sessions.

**Boundary:** A runtime may expose richer native detail beneath the portable status.

<br>

## At a Glance

- **Must** — support every completion claim with current proportional Evidence *(1)*
- **Never** — infer success from missing or inconclusive Evidence *(1)*
- **Must** — make material execution, drift, health, blockers, and Human actions inspectable *(2)*
- **Never** — expose secrets or require hidden reasoning *(2)*
- **Must** — use declared statuses whose changes are established by Observation *(3)*

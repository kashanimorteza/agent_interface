# Foundation Files

This document explains the Foundation directory: what it holds, why those files are shared by the whole Interface, and who may change them. It is Human-owned and explains; it does not redefine. The canonical definition remains `interface.md` in this same directory, which describes the complete system; this document describes only this directory and its contents.

Foundation is not one of the three Modules (Target, Implementation, Agent). It is the set of shared resources those Modules and every Skill depend on.

<br>

## Purpose

Foundation Files provide the foundational definitions and schemas required by the Interface: the canonical Interface document that every Understanding starts from, the Schemas that define how authored and generated files are shaped, and the Config records that coordinate the Workflow.

<br>

## Structure

```text
.interface/foundation/
├── interface.md
├── guide.md
├── personality/
├── action/
├── route/
├── config/
│   ├── application.yaml
│   ├── state.yaml
│   ├── plan.yaml
│   └── review.yaml
└── schema/
    ├── application.yaml
    ├── yaml.yaml
    ├── principles.md
    ├── preferences.yaml
    ├── agent-profile.yaml
    ├── skill-contract.md
    ├── state.yaml
    ├── plan.yaml
    └── review.yaml
```

<br>

## Interface file

[`interface.md`](interface.md) is the canonical definition, navigation entry point, and complete file map of Agent Interface. Interface Understanding — required by every Skill — starts exclusively from this file and follows only the routes it provides for the active role. For every operation except Agent Sync, those routes lead to Target, Implementation, Foundation, Config, and synchronized Runtime resources; seeing the Agent Structure in this file never authorizes entry into the Agent Module.

<br>

## Config

Config stores the mutable operational records used while executing the Interface. It coordinates the Workflow and records where work stands; it does not store what the Target means and never becomes a second project definition.

- [`config/application.yaml`](config/application.yaml) — **Application Manifest**: one public metadata section for every Implementation Component; sections may remain empty until their owners publish metadata.
- [`config/state.yaml`](config/state.yaml) — **State**: active Workflow position, aggregate phase progress, Implement and Launch results, access points, History, Blockers, and Open Questions.
- [`config/plan.yaml`](config/plan.yaml) — **Plan**: Plans, Groups, Tasks, their dependencies, status, and history.
- [`config/review.yaml`](config/review.yaml) — **Review**: reviewed phases, outcomes, Findings, evidence, and Finding status.

`config/` is the only mutable exception in the otherwise read-only `.interface/` tree. Configure creates these files from their Schemas; afterwards each Skill writes only the records it has authority over, always under the rules of the owning Component (Plan, Review, or State).

<br>

## Schema

Schemas define the structure followed by authored Interface files and generated operational records. Two kinds exist:

**Structure standards** — the shape a Human-authored file follows:

- [`schema/yaml.yaml`](schema/yaml.yaml) — the common outer frame (meta, policy, read_order, content_map, content) followed by Implementation Preferences, Agent Profiles, and Config files.
- [`schema/principles.md`](schema/principles.md) — the common Markdown structure of every Implementation and Agent Component `principles.md`.
- [`schema/preferences.yaml`](schema/preferences.yaml) — the four-section structure of every Implementation `preferences.yaml`.
- [`schema/agent-profile.yaml`](schema/agent-profile.yaml) — the three-section structure of every Agent `profile.yaml`.
- [`schema/skill-contract.md`](schema/skill-contract.md) — the portable, runtime-independent structure of every Agent Skill Contract.

**Operational formats** — the stored structure and initial template of a generated record:

- [`schema/application.yaml`](schema/application.yaml) → generates `config/application.yaml`.
- [`schema/state.yaml`](schema/state.yaml) → generates `config/state.yaml`.
- [`schema/plan.yaml`](schema/plan.yaml) → generates `config/plan.yaml`.
- [`schema/review.yaml`](schema/review.yaml) → generates `config/review.yaml`.

Schema definition files use their own formats and do not follow the outer YAML frame they define.

<br>

## Personality, Action, and Route

Three further directories hold shared Human-owned definitions that are neither Config nor Schema. Their structure exists; their content and use are still being defined with the Human.

- [`personality/`](personality/guide.md) — the personalities an Agent can take on (Developer, Planner, Analyst, Reviewer, Architect), one Markdown file each.
- [`action/`](action/guide.md) — the kinds of work an Agent can be asked to do (Develop, Analyze, Review, Plan), one Markdown file each, defining for the model what that work means.
- [`route/`](route/guide.md) — routing: for each Action, the ordered list of models by priority, declared in [`route/route.yaml`](route/route.yaml).

<br>

## Ownership

The Human owns `interface.md`, this document, every Schema, and every file under `personality/`, `action/`, and `route/`. Config records belong to the Components that own them — Plan, State, and Review — and are written only by the Skills the Interface authorizes for each record. Target definitions are intentionally not Foundation Files; they belong to the Target Module.

<br>

## Understanding record

Not yet recorded. The Human's own explanation of Foundation — why the Interface file is the single entry point, how Schemas are meant to evolve, and what Config must never become — will be captured here in a later session, in the same form as the Agent Module Guide.

<br>

## Open decisions

None recorded yet.

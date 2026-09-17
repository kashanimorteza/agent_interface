# Route

This directory holds routing: which model, in which order of preference, should receive each kind of work. A route says, for an Action, "send this first to this model, then to this one, then to this one". Routing is Human-owned and lives under Foundation because it is a shared operational preference, not a Module.

<br>

## Contents

```text
route/
├── guide.md
└── route.yaml
```

- [`route.yaml`](route.yaml) — the routing table: for each Action, an ordered list of models by priority. Currently a skeleton with no routes declared.

<br>

## What is not yet decided

Recorded on 2026-09-17. The Human asked for the structure first; the following are deliberately open:

- The exact shape of a route entry (model identity, provider, fallback rule, conditions).
- Whether routing is by Action only, or by Action and Personality together.
- Who reads the routing table and at what moment (before delegation, at Skill invocation, at Agent Sync).
- How this relates to `agent/runtime/profile.yaml` (`models`, `fallback_models`, `effort_levels`), which is currently empty.

<br>

## Understanding record

Not yet recorded.

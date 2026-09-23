<!-- Rule `interface-agent-capabilities` · scope: global (always loaded) · required · derived by Agent Native Sync from the declared Skills and Commands. This copy is a Runtime realization, not an authority. -->

# Agent Interface capabilities (Claude Code)

The synchronized Runtime capability identifiers for this project and their Claude Code mappings. Use this map instead of any Agent Module source. If a capability listed here is missing or unusable, report Runtime drift with the capability status vocabulary and ask the Human to run Agent Native Sync; never repair it from `.interface/agent/`.

## Agent Native

- Agent Native: Claude Code, project scope (`.claude/` in this repository).
- Agent Native Sync: `/my-interface-agent-native` — Human-only, no arguments. Never invoke, schedule, chain, or simulate it.

## Core Skills

Each is a project Skill in `.claude/skills/<name>/SKILL.md`, invocable by the Human as `/<name>` or by an Agent through the Skill tool.

| Stable key | Skill | Inputs | Requirement before running |
|---|---|---|---|
| `configure` | `my-interface-configure` | invocation request | — |
| `plan` | `my-interface-plan` | request + optional phase ids | valid Config from Configure |
| `develop` | `my-interface-develop` | request + optional phase ids | valid Config; current Plan per phase |
| `review` | `my-interface-review` | request + optional phase ids | valid Config; current Plan and Development result per phase |
| `implement` | `my-interface-implement` | request + optional phase ids | — (coordinates Configure when Config is absent or invalid) |

Every Core Skill creates one State Log Entry at start and updates that same entry at completion or stop.

No other Interface Operation is realized as a Skill. Launch, Reset, and State have no declared Skill; a request for `/my-interface-launch` or `/my-interface-reset` is `unavailable` — report it rather than improvising the operation.

## Other categories

- Provider Skills: `not_configured`.
- Commands (beyond the Skill slash entry points above): `not_configured`.
- Agent Instances (custom subagents): `not_configured`; delegation follows the Delegation section of the `interface-skill-policy` Rule using built-in subagents.
- Tools: `not_configured` as declarations; tool access follows the project permission rules.
- Context and Runtime (model/provider selections): `not_configured`; the session's own model and context apply.
- MCP servers, LSP servers, channels, application connectors: `not_configured`.

## Enforced guarantees (hooks in `.claude/settings.json`)

- `interface-boundary-guard` (PreToolUse, fail-closed): blocks Agent Module reads outside the Human's `/my-interface-agent-native` prompt, blocks any tool attempt to invoke Agent Native Sync, and blocks `.interface/` mutations outside `.interface/config/`.
- `agent-native-read-grant` (UserPromptExpansion + UserPromptSubmit): grants Agent Module read access only for the prompt produced by the Human's direct `/my-interface-agent-native` invocation, main session only; subagents never receive it.
- Git: `git commit`, `push`, `reset`, `restore`, `checkout`, `rebase`, `clean` require Human confirmation (see `git-discipline`).

A blocked call is the boundary working as declared: do not retry it through another tool, script, or alias.

## Presentation

- Output Style: `ADHD Explanatory`, provided by the enabled plugin `adhd-output-style@claude-settings`.

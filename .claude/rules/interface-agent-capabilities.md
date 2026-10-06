> Rule `interface-agent-capabilities` · Scope: **global** — applies to every session and all work in this project, with no path condition. Native realization (derived); regenerated only by `/my-interface-native-implement`.

# Interface Agent capabilities

These are the realized Runtime capability identifiers and their Claude Code mappings. Use them as listed. If one is missing or unusable, report Runtime drift with its Capability Status and ask the Human to run `/my-interface-native-implement`; never resolve it from Executor Module sources.

## Core Skills

Each Core Skill is a project Skill in `.claude/skills/<skill-name>/` and is invoked as `/<skill-name>`. Every Core Skill execution creates one State Log Entry and completes that same Entry with outcome, report, and any data, Open Questions, or Blockers.

| Stable key | Skill name | Invoked by | Inputs |
|---|---|---|---|
| `configure` | `my-interface-configure` | Human or Agent | invocation request |
| `plan` | `my-interface-plan` | Human or Agent | invocation request, optional phase selection |
| `develop` | `my-interface-develop` | Human or Agent | invocation request, optional phase selection |
| `review` | `my-interface-review` | Human or Agent | invocation request, optional phase selection |
| `implement` | `my-interface-implement` | Human or Agent | invocation request, optional phase selection |
| `launch` | `my-interface-launch` | Human or Agent | invocation request, optional scope |
| `reset` | `my-interface-reset` | **Human only** (model invocation disabled) | invocation request, exactly one scope |

- Outputs: every Core Skill returns its execution result and status; `implement` also returns the aggregate counts of associated Open Questions and Blockers.
- Coordination: `implement` coordinates `configure` (only when Config is absent or invalid), then `plan`, `develop`, and `review` per phase, passing its own Log Entry ID as each coordinated Skill's `parent_id`.

## Provider Skills

- `graphify` — knowledge-graph Skill supplied by the graphify package (`.claude/skills/graphify/`, CLI `graphify`); turns project files into a queryable graph used for codebase questions. Invoked as `/graphify`.

## Commands

- No separate Agent Commands are declared. Core Skills are the slash entry points listed above.
- `/my-interface-native-implement` — Agent Native Implement. Invoked **only directly by the Human**. Never invoke, schedule, chain, or simulate it.

## Agent Instances

- No specialized Agent Instances are declared. Delegation uses Claude Code's built-in subagents under the Delegation section of the `interface-skill-policy` Rule.

## Enforced Guarantees (Permission)

| Guarantee | Claude Code mechanism |
|---|---|
| `interface-boundary-guard` — blocks Executor Module reads and searches outside the direct-Human Agent Native Implement prompt, blocks every non-Human invocation of Agent Native Implement, and blocks direct Interface mutation; fails closed | `PreToolUse` hook `.claude/hooks/interface-guard.sh pretooluse` |
| `agent-native-read-grant` — records a session- and prompt-bound, non-transferable read grant only when the Human directly invokes `/my-interface-native-implement`; fails closed | `UserPromptSubmit` hook `interface-guard.sh grant`; revoked by `Stop` / `SessionEnd` hooks `interface-guard.sh revoke` |
| `graphify-guard` — guides searches and reads toward the knowledge graph when it exists; never blocks; fails open | `PreToolUse` hooks `graphify hook-guard search` / `graphify hook-guard read` |

When the boundary guard rejects an action, treat the message as the boundary: do not retry through another tool, path form, script, or alias.

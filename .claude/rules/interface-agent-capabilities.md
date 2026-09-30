<!-- Agent Rule `interface-agent-capabilities` · scope: global (always loaded) · required · derived by Agent Native Sync from the Skill Definition, the Skill Contracts, and the Command Preferences; synchronized Runtime realization, not an authority over the Human-owned declarations. -->

# Agent Interface capabilities

Synchronized Runtime capability identifiers and their Claude Code mappings. Use this map to find a capability; never resolve a capability through `.interface/agent/`. If a capability listed here is missing or unusable, report Runtime drift with its Capability Status and ask the Human to run `/my-interface-agent-native`.

## Core Skills (Constructed)

Each Core Skill is a self-contained Claude Code Skill. Each may be invoked directly by the Human (`/<skill name>`) or by an Agent (Skill tool).

| Stable key | Skill name | Human invocation | Native artifact |
|---|---|---|---|
| `configure` | `my-interface-configure` | `/my-interface-configure` | `.claude/skills/my-interface-configure/SKILL.md` |
| `plan` | `my-interface-plan` | `/my-interface-plan [phase ...]` | `.claude/skills/my-interface-plan/SKILL.md` |
| `develop` | `my-interface-develop` | `/my-interface-develop [phase ...]` | `.claude/skills/my-interface-develop/SKILL.md` |
| `review` | `my-interface-review` | `/my-interface-review [phase ...]` | `.claude/skills/my-interface-review/SKILL.md` |
| `implement` | `my-interface-implement` | `/my-interface-implement [phase ...]` | `.claude/skills/my-interface-implement/SKILL.md` |

- Every Core Skill is required.
- `implement` is the coordinating Skill: it coordinates `configure`, `plan`, `develop`, and `review` and passes its own State Log Entry ID to each as `parent_id`. Coordination never makes another Core Skill optional.

## Provider Skills (Installed)

None are declared.

## Commands

No Command is declared (`not_configured`). The slash entries above are the Core Skills' own invocations, not separate Commands.

## Agent Native Sync

`/my-interface-agent-native` is started only by the Human typing it directly. No Agent, Skill, subagent, hook, or automation may invoke it. This is enforced by the `interface-boundary-guard` and `agent-native-read-grant` hooks (`.claude/settings.json`, `.claude/hooks/interface_guard.py`).

## Not declared as Skills

Launch, Reset, and State exist as Implementation Operation Components but have no Skill Contract, so no Native Skill realizes them. When a Workflow step names one (for example `/my-interface-launch`), report that no synchronized Skill exists for it and ask the Human how to proceed. Do not improvise it.

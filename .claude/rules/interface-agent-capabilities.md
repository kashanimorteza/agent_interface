<!-- Synchronized Runtime Rule. Scope: global (always loaded). Derived by Agent Native Sync (/my-interface-agent-native) from the Human-owned Skill and Command declarations of the Agent Module. It exposes the synchronized Runtime capability identifiers so ordinary operations never read Agent Module sources. The Agent Module is the authority; this file is its Claude Code realization and is regenerated on every synchronization. -->

# Agent Interface capabilities (synchronized)

Use this map to locate the project's synchronized Interface Skills. Never resolve a capability through `.interface/agent/`. A Skill listed here that Claude Code cannot discover or invoke is **Runtime drift**: report it and ask the Human to run `/my-interface-agent-native`.

## Operation Skills

Realization kind for every entry: Constructed from its owning Operation Component by Agent Native Sync. Each Skill's meaning lives in the owning Component's Definition and Preferences under `.interface/implementation/operations/<key>/`; the Skill file at `.claude/skills/<name>/SKILL.md` carries only invocation and boundary.

| Key | Claude Code Skill | Human invocation | Coordinator invocation | Autonomous | Required |
|---|---|---|---|---|---|
| configure | `my-interface-configure` | `/my-interface-configure` | only `my-interface-implement` | disabled | yes |
| plan | `my-interface-plan` | `/my-interface-plan [phase ...]` | only `my-interface-implement` | disabled | yes |
| develop | `my-interface-develop` | `/my-interface-develop [phase ...]` | only `my-interface-implement` | disabled | yes |
| review | `my-interface-review` | `/my-interface-review [phase ...]` | only `my-interface-implement` | disabled | yes |
| launch | `my-interface-launch` | `/my-interface-launch [api\|presentation\|logic\|complete]` | declared coordinators (`my-interface-implement`) | disabled | yes |
| implement | `my-interface-implement` | `/my-interface-implement [phase ...]` | disabled | disabled | yes |
| reset | `my-interface-reset` | `/my-interface-reset <phase ...\|config\|complete>` | disabled | disabled | yes |

- **Coordinating Skill:** `my-interface-implement` is the selected implementation coordinator. Only it may invoke `my-interface-configure`, `my-interface-plan`, `my-interface-develop`, `my-interface-review`, and `my-interface-launch`, and only through Claude Code's own Skill mechanism. Delegated invocation grants no ownership of another Operation's records or outputs.
- **Primary Operation Skills:** configure, plan, develop, review, implement.
- **Supporting Skills** (any other Skill available in the environment) remain available to every Operation according to their own declarations and the synchronized Rules.
- **External providers, disabled Skills, overrides:** none declared (`not_configured`).

## Agent Native Sync entry point

| Skill | Invocation | Boundary |
|---|---|---|
| `my-interface-agent-native` | `/my-interface-agent-native`, direct Human invocation only, no argument | The only reader of `.interface/agent/`. No Skill, Agent Instance, coordinator, hook, or model-generated action may invoke it or inherit its read grant. Its procedure is defined by `.interface/foundation/agent-native-sync.md`. |

## Commands

No Agent Commands are declared (`not_configured`). Every slash invocation above is the Skill itself, invoked as `/<skill-name>`.

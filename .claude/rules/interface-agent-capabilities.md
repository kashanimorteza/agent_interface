<!-- Rule: interface-agent-capabilities | scope: global (loaded at session start for all work) | required: true | Derived by /my-interface-agent-native from the Skill Definition, Skill Preferences, and Command Preferences. Synchronized Claude Code realization; not an authority. -->

# Agent Interface capabilities

The synchronized Runtime capability identifiers and their Claude Code mappings. Use this Rule instead of any Agent Module read. If a capability listed here is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`.

## Skills

Every Operation-backed Skill is **Constructed** (not Installed): its meaning comes from its owning Operation Component Definition and Preferences under `.interface/implementation/operations/<operation>/`, which the Skill reads at execution. The Skill itself is only the Agent-side bridge.

| Capability | Claude Code Skill / command | Primary | Human | Coordinator | Autonomous | Required |
|---|---|---|---|---|---|---|
| `skills.configure` | `my-interface-configure` → `/my-interface-configure` | yes | enabled | only `my-interface-implement` | disabled | yes |
| `skills.plan` | `my-interface-plan` → `/my-interface-plan [phase ...]` | yes | enabled | only `my-interface-implement` | disabled | yes |
| `skills.develop` | `my-interface-develop` → `/my-interface-develop [phase ...]` | yes | enabled | only `my-interface-implement` | disabled | yes |
| `skills.review` | `my-interface-review` → `/my-interface-review [phase ...]` | yes | enabled | only `my-interface-implement` | disabled | yes |
| `skills.launch` | `my-interface-launch` → `/my-interface-launch [scope]` | no | enabled | declared coordinators | disabled | yes |
| `skills.implement` | `my-interface-implement` → `/my-interface-implement [phase ...]` | yes | enabled (explicit Human only) | disabled | disabled | yes |
| `skills.reset` | `my-interface-reset` → `/my-interface-reset [scope]` | no | enabled (explicit Human only) | disabled | disabled | yes |

- **Selected coordinating Skill:** `skills.implement` (`my-interface-implement`). It may invoke only `skills.configure`, `skills.plan`, `skills.develop`, and `skills.review`, and only through Claude Code's own Skill mechanism; each Operation Component keeps ownership of its records and outputs.
- **Primary Operation invocation:** only `skills.implement` may invoke `skills.configure`, `skills.plan`, `skills.develop`, or `skills.review`. No primary Operation Skill invokes another one otherwise. Supporting Skills remain available to every Operation according to their declarations.
- **Autonomous activation:** disabled for every declared Skill. Use a declared Skill only when the Human explicitly invokes it or a declared coordinator authorized for it invokes it.
- **External providers, disabled Skills, overrides:** none declared (`not_configured`).
- **Agent Native Sync:** `/my-interface-agent-native` is invoked only by the Human. No Skill, Agent Instance, hook, or automation may invoke it.

## Commands

No separate Command declarations exist (`not_configured`). The slash commands above are the Claude Code invocation entry points of the declared Skills.

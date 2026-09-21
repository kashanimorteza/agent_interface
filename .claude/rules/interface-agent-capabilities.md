<!-- Synchronized by /my-interface-agent-native. Scope: global (always loaded). Derived from the Agent Skill Definition, Agent Skill Preferences, and Agent Command Preferences. Native realization only; the Human-owned Agent Module is the authority. Do not edit by hand; re-run /my-interface-agent-native. -->

# Interface Agent capabilities

This is the synchronized Runtime map of the Interface's Agent capabilities. Use it instead of any Agent Module source. If a capability listed here is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`; never resolve it from `.interface/agent/`.

## Interface Skills

Every Skill below is Constructed (not Installed) and Operation-backed. Its owning Operation Component's Definition and Preferences are authoritative for its behavior, inputs, outputs, authority, verification, and stopping conditions; the Skill is only the bridge.

| Key | Invoke | Human | Coordinator | Autonomous | Required | Owning Operation Component |
|---|---|---|---|---|---|---|
| configure | `/my-interface-configure` | enabled | only `my-interface-implement` | disabled | yes | `.interface/implementation/operations/configure/configure.md` + `.yaml` |
| plan | `/my-interface-plan` | enabled | only `my-interface-implement` | disabled | yes | `.interface/implementation/operations/plan/plan.md` + `.yaml` |
| develop | `/my-interface-develop` | enabled | only `my-interface-implement` | disabled | yes | `.interface/implementation/operations/develop/develop.md` + `.yaml` |
| review | `/my-interface-review` | enabled | only `my-interface-implement` | disabled | yes | `.interface/implementation/operations/review/review.md` + `.yaml` |
| launch | `/my-interface-launch` | enabled | declared coordinators only (none currently lists it) | disabled | yes | `.interface/implementation/operations/launch/launch.md` + `.yaml` |
| implement | `/my-interface-implement` | enabled (explicit Human only) | disabled | disabled | yes | `.interface/implementation/operations/implement/implement.md` + `.yaml` |
| reset | `/my-interface-reset` | enabled (explicit Human only) | disabled | disabled | yes | `.interface/implementation/operations/reset/reset.md` + `.yaml` |

- **Selected coordinating Skill:** `implement` (`/my-interface-implement`).
- **Primary Operation Skills:** configure, plan, develop, review, implement.
- **Primary invocation:** only `my-interface-implement` may invoke `my-interface-configure`, `my-interface-plan`, `my-interface-develop`, or `my-interface-review`, and only through Claude Code's own Skill tool. Each Operation Component keeps ownership of its records and outputs.
- **Never invoke any Interface Skill on your own initiative.** A Human request phrased in ordinary words is not an invocation; suggest the slash command instead. The coordinator restriction is enforced by the `interface-boundary-guard` hook.
- **Supporting Skills, external providers, disabled Skills, overrides:** none declared.

## Commands

No Command is declared beyond the Skill invocations above. No aliases or extra routing exist.

## Agent Native Sync

- `/my-interface-agent-native` — the only entry point that reads the Agent Module. Only the Human may invoke it by typing it directly. No Skill, subagent, hook, or model action may invoke it, and its read grant never passes to a subagent. This is enforced by the `agent-native-read-grant` and `interface-boundary-guard` hooks.

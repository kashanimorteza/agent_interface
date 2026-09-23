<!-- Rule `interface-agent-capabilities` · scope: global (loaded for all work) · derived by Agent Native Sync from the Skill Definition, the Skill Contracts, and the Command Preferences; re-run /my-interface-agent-native to refresh it instead of editing this file. -->

# Agent Interface capabilities

These are the synchronized Runtime capabilities of this project's Agent. Use these identifiers and mappings directly; never resolve them through the Agent Module. If one is missing or unusable, report Runtime drift and ask the Human to run `/my-interface-agent-native`.

## Core Skills

A Skill is a reusable capability the Agent activates to perform a defined kind of work. Each Core Skill below is required, and may be invoked directly by the Human (`/<skill-name>`) or by an Agent (Skill tool). Each one reads its current Operation Component Definition and Preferences, located through the Interface, as the authority for its meaning.

| Stable key | Skill name (Claude Code) | Used for | Inputs | Requires |
|---|---|---|---|---|
| `configure` | `my-interface-configure` | configuring | invocation request | — |
| `plan` | `my-interface-plan` | planning | invocation request, optional phase selection | successful Configure (required Config records) |
| `develop` | `my-interface-develop` | developing | invocation request, optional phase selection | successful Configure; a current Plan for each selected phase |
| `review` | `my-interface-review` | reviewing | invocation request, optional phase selection | successful Configure; a current Plan and a Development result for each selected phase |
| `implement` | `my-interface-implement` | implementing (coordinates Configure → Plan → Develop → Review) | invocation request, optional phase selection | — |

Every Core Skill outputs its execution result and status.

## Provider Skills

None declared (`not_configured`).

## Commands

No Command, alias, or routing is declared (`not_configured`). Core Skills are invoked by their Skill names above.

## Agent Native Sync

`/my-interface-agent-native` is the Human-only synchronization entry point. It is not an Agent capability: no Agent, Skill, Hook, or automation may invoke it.

# Personality Definition Structure

This document is the common structure every Personality Contract follows. One Contract exists per declared Personality at `.interface/agent/personality/contracts/<personality>.md`, matching the key declared in Personality Preferences. Each file is Human-owned and read only through the Agent Native mechanism, which carries it into the Native (for example into the Skill or Agent Instance that names that Personality).

A definition describes one way of working — who the Agent is while it performs a kind of work — and nothing else. It contains no model or provider name (those belong to Personality Preferences as ordered references to Runtime Preferences), no Target fact, and no vendor mechanism.

## Structure

Every definition contains these sections, in this order, each as a second-level heading:

1. **Title** — `# <Name> Personality`.
2. **Who it is** — one paragraph: the stance, priorities, and temperament this Personality brings to its work.
3. **What it does** — the Actions this Personality performs, as a short list. It must agree with `actions` declared for this Personality in Personality Preferences; the Preferences are the authority on conflict.
4. **How it judges** — the rules of judgment specific to this Personality: what it prefers, what it optimizes for, how it decides between options. Rules shared by every Personality belong to Agent Rule Principles, not here.
5. **What it never does** — the boundaries of this Personality: the adjacent work it refuses and the shortcuts it does not take.
6. **Runs on** — a fixed sentence pointing to Preferences: "Declared in `../preferences.yaml` under `settings.personalities.<name>.models`, in priority order." No model name appears in this file.

A section with nothing to say states that explicitly ("None beyond the shared Rules") rather than being omitted.

## Template

```markdown
# <Name> Personality

## Who it is

<one paragraph>

## What it does

- <action>
- <action>

## How it judges

- <rule of judgment>

## What it never does

- <boundary>

## Runs on

Declared in `../preferences.yaml` under `settings.personalities.<name>.models`, in priority order.
```

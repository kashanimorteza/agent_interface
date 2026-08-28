---
name: interface-status
description: Report where the agent_interface build stands — active mode and item, per-item plan counts, ready tasks, blockers, and open questions. Use when asked what is in progress, what is blocked, or what to do next.
allowed-tools: Read, Grep, Glob, Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/status.py *)
---

# Interface status

Report the state of the build from `.agent/config/`. Read only — this skill never changes a file.

## Fast path

Run the bundled script for the counts:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/status.py
```

It prints the active mode and item, the phase and task counts of each item's plan, the blockers, and the open questions. It needs `pyyaml`.

If the script fails, or `.agent/config/` is empty, fall back to reading the files yourself in the order `root.yaml` sets under `read_order`.

## What to report

1. Mode and item — `state.yaml → content.active`.
2. Each item's plan separately — `task.yaml → content.plans.<item>`. Backend and frontend never share a plan, and each numbers its own phases from P1.
3. Ready tasks, derived: `status` is `todo` and every id in `depends_on` is `done`.
4. Blockers and open questions — `state.yaml`, each with its id.

## What not to do

- Do not start work. This skill reports; claiming a task is `/develop`.
- Do not answer an open question. That is the human's decision, and an agent that answers one has invented a requirement.
- Do not report a plan as empty without saying why — an empty plan usually means the contract it needs is still a draft.

For the meaning of each status and the protocols around them, see [reference.md](reference.md).

---
name: freeze-contract
description: Check whether a draft contract in an item file is ready to be frozen, and list exactly what is still missing. Use before writing any task, since a task may only name a frozen contract.
allowed-tools: Read, Grep, Glob
---

# Freeze a contract

A task may only name a contract that is frozen (`task.yaml → policy.coverage_rule`). So the question "why can no task be written?" is almost always "what is still missing from this contract?"

This skill answers that. It does not freeze anything — freezing is the human's call.

## Procedure

1. Read the producing item's file (`backend.yaml`) and find the contract under `content.contracts`. Note its version and whether it says draft or frozen.
2. For every operation the contract names, check that each field it carries has a settled **type** and, where it matters, a settled **unit** and **permitted values**. A field described only in prose is not settled.
3. Check the consuming side. `frontend.yaml → content.contracts.consumes` must name the same version. A consumer that cannot name a version is itself a gap.
4. Cross-check every gap against `state.yaml`. Each one must already be an open question with an id. A gap with no question is the finding that matters most — report it and propose the question, but do not write the answer.
5. Report: the contract's version, the gaps by field, the question id covering each, and any gap covered by nothing.

## Verdict

Say one of exactly these:

- **Ready to freeze** — every field is settled and every question that blocked it is answered. Name the human decision still required, because freezing is theirs.
- **Not ready** — list the question ids that must be answered first, in the order that unblocks the most.

Never propose a default for an unsettled field, not even an obvious one. A plausible type in a frozen contract survives into every later phase, and `policy.decision_pending` says a decision the human must make is an open question, not a decision.

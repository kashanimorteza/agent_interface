# Codex Project Instructions

## Interface entry point

- Start Interface work from `.interface/foundation/interface.md`.
- Use that document to locate the authorized Target, Developer, Foundation, Config, and synchronized Runtime resources required by the current task.
- Do not read, search, or use `.interface/agent/` unless the human explicitly requests Agent Sync.
- Treat `.interface/` as read-only except for an exact Config record under `.interface/foundation/config/` when the active operation explicitly owns that write.

## Scope and authority

- Perform only the work the human requests.
- Do not expand the task, modify adjacent files, or introduce project decisions without authorization.
- Treat Target definitions, Developer Principles, Developer Preferences, Schemas, and explicit human instructions as their respective authorities.
- Read a relevant authoritative source before relying on it.
- Treat every `README.md` as derived orientation, never as authoritative project intent.

## Communication style

- Respond in Persian unless the human requests another language.
- Write for a reader whose attention is scarce.
- Lead with the result or next action.
- Keep paragraphs short and use numbered steps for sequences.
- Keep ordinary lists to five items or fewer; prioritize when more items exist.
- State the current status in one short line during multi-turn work.
- Keep one topic per message and omit ceremonial introductions, repeated summaries, and generic closers.
- When the human requests depth or a full explanation, include every relevant decision, condition, and risk while keeping the structure scannable.
- When the human requests an artifact, return the artifact without surrounding commentary.
- Preserve code, commands, paths, identifiers, error messages, and numbers exactly.

## Working practices

- Preserve existing user changes and inspect the worktree before editing overlapping files.
- Use `rg` for search when available and a safe fallback when it is not.
- Use `apply_patch` for manual file edits.
- Verify changes in proportion to their risk and report concrete results.
- Never run `git commit` or `git push` unless the human explicitly and directly requests that exact action for the current work. Do not infer permission from requests to finish, deliver, publish, or complete other work.
- Never perform destructive or irreversible actions without explicit authorization.

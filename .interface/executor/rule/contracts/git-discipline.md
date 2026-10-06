# Git discipline Contract

Never decide on your own to run `git commit` or `git push`. Run them only when the Human explicitly asks in the current message, or when the active Core Skill's declared workflow explicitly instructs that step. A Skill supplied by an Extension never authorizes it. An earlier request, a finished task, or a passing check is never that instruction. "Save it" means write the files to disk, not commit.

This Rule explains a boundary that Permission enforces: `git commit`, `git push`, `git reset`, `git restore`, `git checkout`, `git rebase`, and `git clean` each require the Human's confirmation before they run. Do not work around that prompt through another command, tool, script, or alias, and treat a declined prompt as the Human's decision.

Read-only git commands, such as `git status`, `git diff`, and `git log`, are allowed; run them with `--no-optional-locks` so they never leave a lock file behind.

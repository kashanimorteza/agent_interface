<!-- Rule `git-discipline` · scope: global (loaded for all work; no path condition) · required.
     Human-owned declaration realized in Claude Code by Agent Native Sync (/my-interface-agent-native).
     Change it at its Human-owned source and re-run that synchronization; do not edit this copy.
     Enforced by the `ask` permission rules in .claude/settings.json. -->

# Git discipline Contract

Never run `git commit` or `git push` unless the Human explicitly asks for it in the current message. An earlier request, a finished task, a passing check, or a Skill's workflow is never that request. "Save it" means write the files to disk, not commit.

This Rule explains a boundary that Permission enforces: `git commit`, `git push`, `git reset`, `git restore`, `git checkout`, `git rebase`, and `git clean` each require the Human's confirmation before they run. Do not work around that prompt through another command, tool, script, or alias, and treat a declined prompt as the Human's decision.

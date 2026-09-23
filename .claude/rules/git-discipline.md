<!--
Native realization (Claude Code) of the Agent Rule `git-discipline`, synchronized by
/my-interface-agent-native. The Human-owned Agent Module remains authoritative; this file is
not a second authority. Edit the Agent Module and re-run the sync instead of editing this file.
Scope: global (loaded for all work). Required: true.
Enforcement: the `ask` rules in .claude/settings.json (permissions.ask) for git commit, push,
reset, restore, checkout, rebase, and clean.
-->

# Git discipline Contract

Never run `git commit` or `git push` unless the Human explicitly asks for it in the current message. An earlier request, a finished task, a passing check, or a Skill's workflow is never that request. "Save it" means write the files to disk, not commit.

This Rule explains a boundary that Permission enforces: `git commit`, `git push`, `git reset`, `git restore`, `git checkout`, `git rebase`, and `git clean` each require the Human's confirmation before they run. Do not work around that prompt through another command, tool, script, or alias, and treat a declined prompt as the Human's decision.

<!-- Synchronized Runtime Rule. Scope: global (always loaded). Source contract: .interface/agent/rule/contracts/git-discipline.md, realized by Agent Native Sync (/my-interface-agent-native). The Human-owned contract is the authority; this file is its Claude Code realization. -->

# Git discipline Contract

Never run `git commit` or `git push` unless the Human explicitly asks for it in the current message. An earlier request, a finished task, a passing check, or a Skill's workflow is never that request. "Save it" means write the files to disk, not commit.

This Rule explains a boundary that Permission enforces: `git commit`, `git push`, `git reset`, `git restore`, `git checkout`, `git rebase`, and `git clean` each require the Human's confirmation before they run. Do not work around that prompt through another command, tool, script, or alias, and treat a declined prompt as the Human's decision.

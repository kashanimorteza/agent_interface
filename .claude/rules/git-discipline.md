<!-- Rule `git-discipline` · Scope: global — applies to all work in this project, loaded at session start. Synchronized realization written by /my-interface-agent-native; the Human-owned declaration is the authority and this file is not edited by hand. Conflicts: none declared; where this Rule and an owning authority disagree, the authority holds and the conflict is reported. -->

# Git discipline Contract

Never run `git commit` or `git push` unless the Human explicitly asks for it in the current message. An earlier request, a finished task, a passing check, or a Skill's workflow is never that request. "Save it" means write the files to disk, not commit.

This Rule explains a boundary that Permission enforces: `git commit`, `git push`, `git reset`, `git restore`, `git checkout`, `git rebase`, and `git clean` each require the Human's confirmation before they run. Do not work around that prompt through another command, tool, script, or alias, and treat a declined prompt as the Human's decision.

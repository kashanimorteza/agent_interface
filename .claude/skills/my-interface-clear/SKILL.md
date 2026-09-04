---
name: my-interface-clear
description: Clear Agent Interface when explicitly invoked by deleting everything inside .interface/config/ and the root backend/, frontend/, and database/ directories through the bundled script.
disable-model-invocation: true
---

# Clear the project

Run this command from the repository root:

```bash
python3 .claude/skills/my-interface-clear/scripts/clear.py
```

Do not read `.interface/readme.md`, `.interface/root.yaml`, `project.md`, Config files, Schemas, other Skills, or project code before running it. Do not infer or add deletion targets.

The explicit invocation authorizes only these fixed operations, without another confirmation:

- Delete every entry inside `.interface/config/` while preserving the `config/` directory.
- Delete the root `backend/`, `frontend/`, and `database/` directories when present.

Report the script result briefly. Do not invoke another Skill.

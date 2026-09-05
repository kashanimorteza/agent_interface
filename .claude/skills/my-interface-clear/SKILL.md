---
name: my-interface-clear
description: Preview and, only after explicit user confirmation, clear the fixed generated Agent Interface configuration and project directories.
disable-model-invocation: true
---

# Clear the project

## Workflow

Run the bundled `scripts/clear.py` from the project root. Do not read the Interface root, project definition, configuration, Schema, Principles, or Preferences.

The targets are fixed constants:

- Delete every entry inside `.interface/config/` while preserving the `config/` directory.
- Delete the root `backend/` directory when present.
- Delete the root `frontend/` directory when present.
- Delete the root `database/` directory when present.

First run `scripts/clear.py` without arguments. It only prints the exact targets and changes nothing. Show that list to the user and ask whether those targets should be deleted.

The initial invocation is not approval. Run `scripts/clear.py --apply` only after the user explicitly accepts the displayed deletion list. If the list is empty or the user declines, stop without changing anything.

Perform no discovery and no other workflow operation. After an approved deletion, report the script output in one short sentence.

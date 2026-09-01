---
name: my-interface-clear
description: Clear only the currently mapped generated Agent Interface files after the Developer explicitly requests a reset and confirms the resolved deletion list.
disable-model-invocation: true
---

# Clear generated Interface files safely

Remove only the generated files authorized by the live Interface.

## Refresh context and resolve scope

1. Re-read the repository `README.md` to understand Agent Interface and this Skill's role.
2. Re-read `.interface/root.yaml` as the Interface entry point and resolve all other paths from its current map.
3. Follow that map to read every live policy, authority, and state file needed to determine what the current reset may remove.
4. Derive and enumerate the exact existing deletion set from those files.

Read these sources from disk on every invocation. Do not reuse a path, file list, policy, or parameter from an earlier run or from this Skill.

Do not read the human project-definition file. It is not needed to resolve a generated-file reset.

Show the exact resolved list to the Developer and obtain confirmation in the current run. Invocation alone is not confirmation of a newly resolved deletion scope.

## Delete

After confirmation, delete exactly the confirmed generated files and nothing else. Keep any directory the Interface map says must remain. Do not use an unresolved variable, wildcard, broad recursive target, or remembered path to determine deletion scope.

Treat everything outside the confirmed generated set as out of scope, including every source or authority the live Interface marks as protected or human-managed.

## Completion

Report what was removed, whether the mapped generated area is ready for regeneration, and whether recovery is available. Do not invoke another Skill automatically.

---
name: my-interface-clear
description: Clear only the currently mapped generated Agent Interface files when the Developer explicitly invokes this Skill; the invocation itself authorizes the resolved deletion set without a second confirmation.
disable-model-invocation: true
---

# Clear generated Interface files safely

Remove only the generated files authorized by the live Interface.

## Developer guide

Before performing any other step, read [references/developer-guide.md](references/developer-guide.md) completely and apply it throughout this invocation. The guide may refine execution but cannot expand this Skill's live authority, deletion set, or safety boundaries.

## Refresh context and resolve scope

1. Follow the live Interface map to read every policy, authority, and state file needed to determine what the current reset may remove.
2. Derive and enumerate the exact existing deletion set from those files.

The explicit invocation of this Skill authorizes deletion of the exact currently mapped generated files. Resolve and report that list, then proceed without requesting a second confirmation.

## Delete

Delete exactly the resolved generated files and nothing else. Keep any directory the Interface map says must remain. Do not use an unresolved variable, wildcard, broad recursive target, or remembered path to determine deletion scope.

Treat everything outside the resolved generated set as out of scope, including every source or authority the live Interface marks as protected or human-managed.

## Completion

Report what was removed, whether the mapped generated area is ready for regeneration, and whether recovery is available. Do not invoke another Skill automatically.

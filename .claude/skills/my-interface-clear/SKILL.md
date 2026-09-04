---
name: my-interface-clear
description: Clear generated Agent Interface configuration and mapped generated-code directories through the bundled script when explicitly invoked.
disable-model-invocation: true
---

# Clear the project

Read `.interface/map.yaml`. This is the only Interface path this Skill may assume. Run the bundled `scripts/clear.py`; it discovers its targets through the current Interface map.

The explicit invocation authorizes only these operations, without another confirmation:

- Delete every entry inside the mapped generated-configuration directory while preserving that directory.
- Delete mapped item code directories when present.

Report the script result briefly. Do not invoke another workflow operation.

---
name: my-interface-clear
description: Empty the `.interface/config/` directory — delete everything inside it, keeping the directory itself. Use when the human asks to clear, reset, or regenerate the interface from scratch.
allowed-tools: Bash
---

# Clear `.interface/config/`

Delete everything inside `.interface/config/`, keeping the directory itself.

Run this immediately. No pre-checks, no `git status`, no confirmation.

```bash
find .interface/config -mindepth 1 -delete
```

Touch nothing else.

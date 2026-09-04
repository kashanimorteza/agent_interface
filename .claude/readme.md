# Agent Interface for Claude

This directory contains the Claude-specific integration for Agent Interface. The Interface itself remains agent-independent under `.interface/`; Claude Skills discover its current structure through `.interface/map.yaml`.

## Agent Skills

### `my-interface-interpreter`

`.claude/skills/my-interface-interpreter/SKILL.md`

Transforms the human project definition into the generated project Understanding required by downstream operations.

### `my-interface-tasker`

`.claude/skills/my-interface-tasker/SKILL.md`

Creates or reconciles an implementation-ready plan for one requested project phase without implementing it.

### `my-interface-developer`

`.claude/skills/my-interface-developer/SKILL.md`

Implements and verifies eligible planned Tasks for one requested project phase within its authorized boundaries.

### `my-interface-reviewer`

`.claude/skills/my-interface-reviewer/SKILL.md`

Reviews the implemented result for one requested project phase and reports evidence-based findings without repairing it.

### `my-interface-clear`

`.claude/skills/my-interface-clear/SKILL.md`

Clears generated Interface configuration and mapped generated-code directories through its bundled script.

### `my-interface-reset`

`.claude/skills/my-interface-reset/SKILL.md`

Resets the generated workflow to its pre-development or pre-planning stage while preserving project code and generated Understanding.

### `my-interface-skill-installer`

`.claude/skills/my-interface-skill-installer/SKILL.md`

Discovers and installs compatible Claude Skills for technologies detected in the configured target project.

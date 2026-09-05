#!/usr/bin/env python3
"""Preview or apply a reset: 1 = interpreter, 2 = task, 3 = develop."""

import argparse
from datetime import date
from pathlib import Path
import shutil

import yaml


CONFIG_DIRECTORY = Path(".interface/config")
TASK_FILE = CONFIG_DIRECTORY / "task.yaml"
STATE_FILE = CONFIG_DIRECTORY / "state.yaml"
CODE_DIRECTORIES = tuple(Path(name) for name in ("backend", "frontend", "database", "developer"))
STAGES = {"1": "interpreter", "2": "task", "3": "develop"}


def load(path):
    if not path.is_file():
        raise SystemExit(f"Required file not found: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def save(path, value):
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True, width=120),
        encoding="utf-8",
    )


def entries(value):
    if isinstance(value, dict):
        return value.values()
    if isinstance(value, list):
        return value
    raise SystemExit("Expected a list or mapping in the Task structure; nothing changed.")


def all_tasks(plans):
    for plan in entries(plans):
        for group in entries(plan.get("groups", {})):
            yield from entries(group.get("tasks", {}))


def remove(path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=STAGES, help="1 = interpreter, 2 = task, 3 = develop")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    stage = STAGES[args.stage]

    directories = [p for p in CODE_DIRECTORIES if p.is_dir() or p.is_symlink()]
    config_entries = []
    changes = []
    if stage == "interpreter":
        if CONFIG_DIRECTORY.is_symlink():
            raise SystemExit("Config directory is a symlink; refusing to traverse it.")
        if CONFIG_DIRECTORY.exists():
            config_entries = sorted(CONFIG_DIRECTORY.iterdir())
        changes.extend(f"Delete config entry: {p}" for p in config_entries)
    else:
        task = load(TASK_FILE)
        state = load(STATE_FILE)
        plans = task["content"]["plans"]
        tasks = list(all_tasks(plans))
        if not all(isinstance(item, dict) for item in tasks):
            raise SystemExit("Every Task must be a mapping; nothing changed.")
        if stage == "task":
            group_count = sum(len(p.get("groups", {})) for p in entries(plans))
            changes.append(f"Clear {group_count} Group(s) and {len(tasks)} Task(s) from {TASK_FILE}; preserve Plan shells")
            for plan in entries(plans):
                plan["groups"] = [] if isinstance(plan.get("groups"), list) else {}
            mode = "not set"
        else:
            changes.append(f"Set {len(tasks)} Task(s) to todo and remove their blocker fields in {TASK_FILE}; preserve content and history")
            for item in tasks:
                item["status"] = "todo"
                item.pop("blocker", None)
            mode = "planning"
        state["content"]["active"] = {
            "mode": mode,
            "mode_reason": f"{stage} reset requested by the human.",
            "phase": None,
            "set_by": "reset operation",
            "set_at": date.today().isoformat(),
        }
        changes.append(f"Set active State to {mode} with phase null; preserve shared blockers and questions")

    changes.extend(f"Delete root directory: {p}/" for p in directories)
    if args.apply:
        if stage != "interpreter":
            save(STATE_FILE, state)
            save(TASK_FILE, task)
        for path in config_entries + directories:
            remove(path)

    print(f"RESET {'APPLIED' if args.apply else 'PREVIEW'}: {args.stage} = {stage}")
    for change in changes:
        print(f"- {change}")
    if not args.apply:
        print("No changes made. Re-run with --apply only after explicit user confirmation.")


if __name__ == "__main__":
    main()

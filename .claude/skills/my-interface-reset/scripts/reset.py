#!/usr/bin/env python3
"""Preview or apply the fixed planning and development resets."""

import argparse
from datetime import date
from pathlib import Path
import shutil

import yaml


TASK_FILE = Path(".interface/config/task.yaml")
STATE_FILE = Path(".interface/config/state.yaml")
CODE_DIRECTORIES = (Path("backend"), Path("frontend"), Path("database"))


def load(path):
    if not path.is_file():
        raise SystemExit(f"Required file not found: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def save(path, value):
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True, width=120),
        encoding="utf-8",
    )


def all_tasks(plans):
    for plan in plans.values():
        for group in plan.get("groups", {}).values():
            yield from group.get("tasks", {}).values()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("planning", "development"))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    task = load(TASK_FILE)
    state = load(STATE_FILE)
    plans = task["content"]["plans"]

    if args.stage == "planning":
        group_count = sum(len(plan.get("groups", {})) for plan in plans.values())
        task_count = sum(1 for _ in all_tasks(plans))
        changes = [
            f"Clear {group_count} Group(s) and {task_count} Task(s) from {TASK_FILE}",
            f"Set content.active to null in {STATE_FILE}",
        ]
        if args.apply:
            for plan in plans.values():
                plan["groups"] = {}
            state["content"]["active"] = None
            save(TASK_FILE, task)
            save(STATE_FILE, state)
    else:
        tasks = list(all_tasks(plans))
        directories = [path for path in CODE_DIRECTORIES if path.exists() or path.is_symlink()]
        changes = [
            f"Set content.active to planning / none in {STATE_FILE}",
            f"Set {len(tasks)} Task(s) to todo and remove their blocker fields in {TASK_FILE}",
            *(f"Delete root directory: {path}/" for path in directories),
        ]
        if args.apply:
            state["content"]["active"] = {
                "mode": "planning",
                "mode_reason": "Development reset requested by the human.",
                "phase": "none",
                "set_by": "reset operation",
                "set_at": date.today().isoformat(),
            }
            save(STATE_FILE, state)
            for item in tasks:
                item["status"] = "todo"
                item.pop("blocker", None)
            save(TASK_FILE, task)
            for path in directories:
                if path.is_symlink():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)

    print(f"RESET {'APPLIED' if args.apply else 'PREVIEW'}: {args.stage}")
    for change in changes:
        print(f"- {change}")
    if not args.apply:
        print("No changes made. Re-run with --apply only after explicit user confirmation.")


if __name__ == "__main__":
    main()

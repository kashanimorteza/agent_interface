#!/usr/bin/env python3
"""Print where the agent_interface build stands.

Reads .agent/config/ and writes nothing. Requires pyyaml.
"""
import os
import sys

try:
    import yaml
except ImportError:
    sys.exit("pyyaml is required:  pip install pyyaml")

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
CONFIG = os.path.join(ROOT, ".agent", "config")


def load(name):
    path = os.path.join(CONFIG, name)
    if not os.path.exists(path):
        sys.exit("missing: %s\n.agent/config/ may not have been generated yet — run /configure." % path)
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def as_list(node):
    """phases and groups may be written as a list or as a mapping."""
    if isinstance(node, dict):
        return list(node.values())
    return node or []


def main():
    state = load("state.yaml").get("content", {})
    task = load("task.yaml").get("content", {})

    active = state.get("active", {})
    print("mode : %s" % active.get("mode", "?"))
    print("item : %s" % active.get("item", "?"))

    print("\nplans")
    for item, plan in (task.get("plans") or {}).items():
        phases = as_list(plan.get("phases"))
        tasks = [
            t
            for p in phases
            for g in as_list(p.get("groups"))
            for t in (g.get("tasks") or [])
        ]
        counts = {}
        for t in tasks:
            s = t.get("status", "?")
            counts[s] = counts.get(s, 0) + 1
        ready = sum(
            1
            for t in tasks
            if t.get("status") == "todo"
            and all(
                any(o.get("id") == d and o.get("status") == "done" for o in tasks)
                for d in (t.get("depends_on") or [])
            )
        )
        detail = ", ".join("%s %d" % kv for kv in sorted(counts.items())) or "no tasks"
        print("  %-10s %2d phases  %3d tasks  (%s)  ready: %d"
              % (item, len(phases), len(tasks), detail, ready))

    print("\nblockers")
    for b in as_list(state.get("blockers")) or ["  (none)"]:
        if isinstance(b, dict):
            print("  %-4s %s" % (b.get("id", "?"), b.get("blocks", "")))

    print("\nopen questions")
    for q in as_list(state.get("open_questions")) or ["  (none)"]:
        if isinstance(q, dict):
            print("  %-4s %s" % (q.get("id", "?"), q.get("question", "")))


if __name__ == "__main__":
    main()

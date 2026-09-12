#!/usr/bin/env python3
"""Preview or physically remove explicitly listed Interface Config files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


EXPECTED_CONFIG_SUFFIX = Path(".interface/foundation/config")


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(2)


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate exact Interface Config targets and optionally unlink them."
    )
    parser.add_argument("--config-root", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("files", nargs="+", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_root = args.config_root.expanduser().resolve()

    if not config_root.is_dir():
        fail(f"Config root is not an existing directory: {config_root}")
    if config_root.parts[-3:] != EXPECTED_CONFIG_SUFFIX.parts:
        fail(f"Refusing unexpected Config root: {config_root}")

    targets: list[Path] = []
    seen: set[Path] = set()
    for raw in args.files:
        candidate = raw.expanduser()
        if not candidate.is_absolute():
            candidate = config_root / candidate
        if candidate.is_symlink():
            fail(f"Refusing symlink Config target: {candidate}")
        target = candidate.resolve(strict=False)

        if target == config_root or not is_within(target, config_root):
            fail(f"Target is outside the Config root or is the root itself: {target}")
        if target in seen:
            fail(f"Duplicate Config target: {target}")
        if target.exists() and not target.is_file():
            fail(f"Config target is not a file: {target}")

        seen.add(target)
        targets.append(target)

    result: dict[str, object] = {
        "mode": "apply" if args.apply else "preview",
        "config_root": str(config_root),
        "targets": [str(target) for target in targets],
    }

    if not args.apply:
        result["existing"] = [str(target) for target in targets if target.exists()]
        result["already_absent"] = [
            str(target) for target in targets if not target.exists()
        ]
        print(json.dumps(result, indent=2))
        return

    removed: list[str] = []
    already_absent: list[str] = []
    for target in targets:
        if target.exists():
            target.unlink()
            removed.append(str(target))
        else:
            already_absent.append(str(target))

    remaining = [str(target) for target in targets if target.exists()]
    result.update(
        removed=removed,
        already_absent=already_absent,
        remaining=remaining,
        outcome="completed" if not remaining else "failed",
    )
    print(json.dumps(result, indent=2))
    if remaining:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

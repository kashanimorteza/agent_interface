from __future__ import annotations

import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path.cwd()
CONFIG_DIR = PROJECT_ROOT / ".interface" / "config"
PROJECT_DIRS = tuple(PROJECT_ROOT / name for name in ("backend", "frontend", "database"))


def remove_entry(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def find_targets() -> list[Path]:
    if CONFIG_DIR.is_symlink():
        raise RuntimeError("Refusing to clear a symlinked generated-configuration directory.")
    if CONFIG_DIR.exists() and not CONFIG_DIR.is_dir():
        raise RuntimeError(".interface/config is not a directory.")

    targets: list[Path] = []
    if CONFIG_DIR.is_dir():
        targets.extend(sorted(CONFIG_DIR.iterdir()))

    for directory in PROJECT_DIRS:
        if directory.is_symlink() or directory.is_dir():
            targets.append(directory)

    return targets


def main() -> None:
    if sys.argv[1:] not in ([], ["--apply"]):
        raise SystemExit("Usage: clear.py [--apply]")

    targets = find_targets()
    if not targets:
        print("Nothing to clear.")
        return

    if not sys.argv[1:]:
        print("Targets:")
        for path in targets:
            print(f"- {path.relative_to(PROJECT_ROOT)}")
        return

    for path in targets:
        remove_entry(path)
    print("Removed: " + ", ".join(str(path.relative_to(PROJECT_ROOT)) for path in targets))


if __name__ == "__main__":
    main()

from __future__ import annotations

import shutil
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_PATH.parents[4]
CONFIG_DIR = PROJECT_ROOT / ".interface" / "config"
PROJECT_DIRECTORIES = tuple(PROJECT_ROOT / name for name in ("backend", "frontend", "database"))


def remove_entry(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def main() -> None:
    expected_script = PROJECT_ROOT / ".claude" / "skills" / "my-interface-clear" / "scripts" / "clear.py"
    if SCRIPT_PATH != expected_script.resolve():
        raise RuntimeError("Clear script is not inside the expected project skill path.")

    removed: list[str] = []

    if CONFIG_DIR.is_symlink():
        raise RuntimeError("Refusing to clear a symlinked .interface/config directory.")
    if CONFIG_DIR.exists() and not CONFIG_DIR.is_dir():
        raise RuntimeError(".interface/config exists but is not a directory.")
    if CONFIG_DIR.is_dir():
        for entry in list(CONFIG_DIR.iterdir()):
            remove_entry(entry)
            removed.append(str(entry.relative_to(PROJECT_ROOT)))

    for directory in PROJECT_DIRECTORIES:
        if directory.is_symlink():
            directory.unlink()
            removed.append(str(directory.relative_to(PROJECT_ROOT)))
        elif directory.is_dir():
            shutil.rmtree(directory)
            removed.append(str(directory.relative_to(PROJECT_ROOT)))

    if removed:
        print("Removed: " + ", ".join(removed))
    else:
        print("Nothing to clear.")


if __name__ == "__main__":
    main()

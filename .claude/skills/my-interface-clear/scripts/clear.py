from __future__ import annotations

import os
import shutil
from pathlib import Path

import yaml


SCRIPT_PATH = Path(__file__).resolve()
INTERFACE_ROOT_PATH = Path(".interface/root.yaml")


def find_project_root() -> Path:
    for directory in (SCRIPT_PATH.parent, *SCRIPT_PATH.parents):
        if (directory / INTERFACE_ROOT_PATH).is_file():
            return directory
    raise RuntimeError("Cannot locate the Agent Interface root file.")


PROJECT_ROOT = find_project_root()
ROOT_FILE = PROJECT_ROOT / INTERFACE_ROOT_PATH


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        value = yaml.safe_load(stream)
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected a mapping in {path.relative_to(PROJECT_ROOT)}.")
    return value


def project_path(value: str) -> Path:
    relative = Path(value)
    if relative.is_absolute():
        raise RuntimeError(f"Refusing absolute mapped path: {value}")

    root = Path(os.path.abspath(PROJECT_ROOT))
    candidate = Path(os.path.abspath(PROJECT_ROOT / relative))
    if candidate == root or root not in candidate.parents:
        raise RuntimeError(f"Mapped path escapes or equals the repository root: {value}")
    return candidate


def discover_targets() -> tuple[Path, tuple[Path, ...]]:
    root = load_yaml(ROOT_FILE)
    try:
        mapped = root["content"]["files_and_folders"]
        config_dir = project_path(mapped["config"]["path"])
        schema = mapped["schema"]
        schema_dir = project_path(schema["path"])
        schema_files = schema["files"]
    except (KeyError, TypeError) as error:
        raise RuntimeError("The Interface root map does not expose the required generated configuration and Schema entries.") from error

    code_paths: set[Path] = set()
    for entry in schema_files:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            continue
        schema_file = project_path(str(schema_dir.relative_to(PROJECT_ROOT) / entry["path"]))
        if not schema_file.is_file():
            continue
        document = load_yaml(schema_file)
        code_path = document.get("preferences", {}).get("defaults", {}).get("code_path")
        if isinstance(code_path, str) and code_path.strip():
            candidate = project_path(code_path)
            if candidate == ROOT_FILE.parent or candidate == config_dir:
                raise RuntimeError(f"Refusing unsafe mapped code path: {code_path}")
            code_paths.add(candidate)

    return config_dir, tuple(sorted(code_paths))


def remove_entry(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def main() -> None:
    config_dir, project_directories = discover_targets()

    removed: list[str] = []

    if config_dir.is_symlink():
        raise RuntimeError("Refusing to clear a symlinked generated-configuration directory.")
    if config_dir.exists() and not config_dir.is_dir():
        raise RuntimeError("The mapped generated-configuration path is not a directory.")
    if config_dir.is_dir():
        for entry in list(config_dir.iterdir()):
            remove_entry(entry)
            removed.append(str(entry.relative_to(PROJECT_ROOT)))

    for directory in project_directories:
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

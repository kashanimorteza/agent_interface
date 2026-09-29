"""Derivation and validation of Entity Service identities."""

from collections.abc import Iterable

from logic.core.identifiers import check_identifiers, pascal_case, snake_case

CHILD_FILE = "<entity>"
CHILD_STRUCTURE = "<entity><child_suffix>"
CHILD_SUFFIX = "Service"
BASE_STRUCTURE = "BaseEntity"


def child_identities(
    entities: Iterable[str],
    file_pattern: str = CHILD_FILE,
    structure_pattern: str = CHILD_STRUCTURE,
    suffix: str = CHILD_SUFFIX,
    base: str = BASE_STRUCTURE,
) -> dict[str, tuple[str, str]]:
    """Derive and validate the Child Service file and public structure of every Entity.

    Args:
        entities (Iterable[str]): Entity names in Target order.
        file_pattern (str): Pattern for a Child file name.
        structure_pattern (str): Pattern for a Child public structure name.
        suffix (str): Child suffix substituted into the structure pattern.
        base (str): Name of the Base Entity structure.

    Returns:
        (dict[str, tuple[str, str]]): For each Entity name, its file name and structure name.
    """
    names = tuple(entities)
    files = [file_pattern.replace("<entity>", snake_case(name)) for name in names]
    structures = [
        structure_pattern.replace("<entity>", pascal_case(name)).replace(
            "<child_suffix>", suffix
        )
        for name in names
    ]
    check_identifiers(files, "Child file")
    check_identifiers([*structures, base], "Child structure", normalize=str.strip)
    return dict(zip(names, zip(files, structures, strict=True), strict=True))

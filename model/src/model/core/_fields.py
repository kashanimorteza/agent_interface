"""Private constructors for the two mandatory Fields every Entity carries."""

from model.core.declaration import FieldDeclaration


def identity() -> FieldDeclaration:
    """The mandatory id: non-nullable, immutable, integer with Auto Increment."""
    return FieldDeclaration(
        "id",
        "integer",
        nullable=False,
        immutable=True,
        value_generation="auto_increment",
    )


def activity(description: str) -> FieldDeclaration:
    """The mandatory is_active: non-nullable, mutable, Boolean defaulting to true."""
    return FieldDeclaration(
        "is_active",
        "boolean",
        nullable=False,
        description=description,
        has_default=True,
        default=True,
    )

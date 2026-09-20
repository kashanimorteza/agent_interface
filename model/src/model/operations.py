"""The Operations Model offers on its Public Interface.

Each Operation is a complete unit of work named in the consumer's terms. Model stores nothing,
performs no application behaviour and offers no stored-data operation, so none appears here.
"""

from collections.abc import Mapping
from typing import Any

from model.declaration import Declaration
from model.foundation import ModelFoundation


def _require_definition(definition: object) -> None:
    if not (isinstance(definition, type) and issubclass(definition, ModelFoundation)):
        raise TypeError(f"{definition!r} is not a Domain Definition")


def describe(definition: type[ModelFoundation]) -> Declaration:
    """Read everything a Domain Definition has declared about itself.

    Accepts: a Domain Definition.
    Returns: its Declaration — persistence, every Field with its terms, every relationship with
    the referenced definition itself, and its composite uniqueness sets.
    Outcomes: the Declaration; `TypeError` when the argument is not a Domain Definition.
    """
    _require_definition(definition)
    return definition.declaration()


def create[T: ModelFoundation](definition: type[T], **values: Any) -> T:
    """Construct a validated instance of a Domain Definition from named values.

    Accepts: a Domain Definition and one named value per Field it requires.
    Returns: the validated instance.
    Outcomes: the instance; `pydantic.ValidationError` naming each Field whose value breaks a
    rule, is missing, or is not a Field of the definition; `TypeError` when the first argument
    is not a Domain Definition.
    """
    _require_definition(definition)
    return definition(**values)


def serialize(instance: ModelFoundation) -> dict[str, Any]:
    """Convert an instance to its Plain Representation.

    Accepts: an instance of a Domain Definition.
    Returns: every Field as a simple, JSON-compatible named value. A relationship appears only
    as its reference value, and no Field is withheld.
    Outcomes: the Plain Representation; `TypeError` when the argument is not an instance of a
    Domain Definition.
    """
    if not isinstance(instance, ModelFoundation):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise TypeError(f"{instance!r} is not an instance of a Domain Definition")
    return instance.serialize()


def deserialize[T: ModelFoundation](definition: type[T], data: Mapping[str, Any]) -> T:
    """Create a validated instance from a Plain Representation.

    Accepts: a Domain Definition and a Plain Representation of it.
    Returns: the validated instance, under the same rules as construction.
    Outcomes: the instance; `pydantic.ValidationError` naming each Field that breaks a rule;
    `TypeError` when the first argument is not a Domain Definition.
    """
    _require_definition(definition)
    return definition.deserialize(data)

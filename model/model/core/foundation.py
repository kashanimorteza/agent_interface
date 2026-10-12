"""The public Foundation contract: lossless conversion between an Entity and its JSON Object."""

import json
from typing import Any, Self

from pydantic import ValidationError
from pydantic_core import InitErrorDetails, PydanticCustomError
from pydantic_core import to_json as json_text

from model.core._base import HIDDEN, Base


class _Refused(ValueError):
    pass


def _without_repeated_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    keys = [key for key, _ in pairs]
    if len(set(keys)) != len(keys):
        raise _Refused("a key is repeated")
    return dict(pairs)


def _no_constant(name: str) -> Any:
    raise _Refused(f"non-standard constant {name}")


def _decode(text: object) -> tuple[dict[str, Any] | None, str | None]:
    if not isinstance(text, str):
        return None, "input should be JSON text"
    try:
        root = json.loads(
            text, object_pairs_hook=_without_repeated_keys, parse_constant=_no_constant
        )
    except _Refused as refusal:
        return None, str(refusal)
    except json.JSONDecodeError as error:
        return None, f"{error.msg} at line {error.lineno} column {error.colno}"
    except ValueError:
        return None, "a number is too large"
    if not isinstance(root, dict):
        return None, "the root should be one object"
    return root, None


class Foundation(Base):
    """Every Entity extends Foundation and converts to and from its JSON Object."""

    def to_json(self) -> str:
        """Return JSON text whose root object holds exactly the Fields, in Declaration order."""
        values = {name: getattr(self, name) for name in type(self).model_fields}
        return json_text(values).decode()

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Build an Entity from JSON text with the same rules as direct construction.

        An Auto Increment value present in the JSON Object is accepted as the value
        storage assigned, so a stored Entity rebuilds from its JSON Object.
        """
        root, reason = _decode(text)
        if root is None:
            marked = any(
                field.sensitivity is not None for field in cls.declaration.fields
            )
            raise ValidationError.from_exception_data(
                cls.__name__,
                [
                    InitErrorDetails(
                        type=PydanticCustomError(
                            "json_invalid",
                            "Invalid JSON: {reason}",
                            {"reason": reason or ""},
                        ),
                        loc=(),
                        input=HIDDEN if marked else text,
                    )
                ],
            )
        return cls._validated(root, json_object=True)

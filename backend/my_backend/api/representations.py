"""What the contract accepts and returns, built from the shared definitions.

None of this is written out by hand. Each shape is derived from the definition
it belongs to, so a field keeps the meaning it was given and a change to a
definition reaches the contract without anything here being edited.

Three shapes per kind of data, because three different things are being said:
what must be supplied to bring a record into being, what may be supplied to
change one, and what comes back. The last of those never contains a credential.
"""

from __future__ import annotations

from typing import Any

from my_model import Entity, is_stated
from pydantic import BaseModel, ConfigDict, create_model


def credential_fields(definition: type[Entity]) -> set[str]:
    """The fields this definition marks as credentials.

    Read from the definition, never guessed from the name: what a field is
    called is not evidence of what it holds.
    """

    return set(definition.credential_fields())


def _assigned_by_storage(definition: type[Entity], field_name: str) -> bool:
    spec = definition.entity_fields[field_name]
    return bool(is_stated(spec.auto_increment) and spec.auto_increment)


def input_shape(definition: type[Entity]) -> type[BaseModel]:
    """What must be supplied to bring one record into being.

    Credentials belong here — this is the direction they are allowed to travel.
    What the storing layer assigns does not.
    """

    fields: dict[str, Any] = {}
    for name, field in definition.model_fields.items():
        if _assigned_by_storage(definition, name):
            continue
        fields[name] = (field.annotation, field.default if not field.is_required() else ...)

    return create_model(
        f"{definition.entity_name}Input",
        __config__=ConfigDict(extra="forbid", title=f"{definition.entity_name} to create"),
        **{name: (annotation, default) for name, (annotation, default) in fields.items()},
    )


def change_shape(definition: type[Entity]) -> type[BaseModel]:
    """What may be supplied to change one record.

    Everything is optional here, because a change states only the fields it
    means to change. A field left out is left alone.
    """

    fields: dict[str, Any] = {}
    for name, field in definition.model_fields.items():
        if _assigned_by_storage(definition, name):
            continue
        fields[name] = (field.annotation | None, None)

    return create_model(
        f"{definition.entity_name}Change",
        __config__=ConfigDict(extra="forbid", title=f"{definition.entity_name} changes"),
        **fields,
    )


def output_shape(definition: type[Entity]) -> type[BaseModel]:
    """What comes back for one record.

    A credential is absent from this shape, which is what keeps it out of both
    the response and the description of the response.
    """

    withheld = credential_fields(definition)
    fields: dict[str, Any] = {}
    for name, field in definition.model_fields.items():
        if name in withheld:
            continue
        annotation = field.annotation
        if _assigned_by_storage(definition, name) or not field.is_required():
            annotation = annotation | None
        fields[name] = (annotation, None)

    return create_model(
        f"{definition.entity_name}",
        __config__=ConfigDict(title=definition.entity_name),
        **fields,
    )


class Shapes:
    """The three shapes one kind of data is carried in."""

    __slots__ = ("definition", "incoming", "change", "outgoing", "withheld")

    def __init__(self, definition: type[Entity]) -> None:
        self.definition = definition
        self.incoming = input_shape(definition)
        self.change = change_shape(definition)
        self.outgoing = output_shape(definition)
        self.withheld = credential_fields(definition)

    def present(self, record: Any) -> BaseModel:
        """One stored record, in the shape the contract returns."""

        values = record.stated_fields() if hasattr(record, "stated_fields") else dict(record)
        return self.outgoing.model_validate(
            {name: value for name, value in values.items() if name not in self.withheld}
        )


__all__ = [
    "Shapes",
    "change_shape",
    "credential_fields",
    "input_shape",
    "output_shape",
]

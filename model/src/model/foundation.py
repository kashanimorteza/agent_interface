"""Model Foundation: shared, technology-independent mechanisms for every Domain Definition.

Provides validation, serialization, and metadata-publishing mechanisms common to every
concrete Model realization without owning, injecting, or requiring a Field or Domain
Relationship on any of them (Model Principle 4).
"""

import typing
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field
from pydantic_core import PydanticUndefined


def domain_field(
    default: Any = ...,
    *,
    description: str,
    length: int | None = None,
    precision: tuple[int, int] | None = None,
    primary_key: bool = False,
    auto_increment: bool = False,
    unique: bool = False,
    index: bool = False,
    foreign_key: str | None = None,
    cardinality: str | None = None,
    credential: str | None = None,
    nullable: bool | None = None,
    **kwargs: Any,
) -> Any:
    """Declare one Model Field, carrying its technology-independent vocabulary (Model Principle 9)
    alongside its Pydantic definition.

    `nullable` states whether persistence may store null for the field. It defaults to what the
    field's own type annotation implies (an `X | None` annotation is nullable); pass it explicitly
    only when the persisted column's declared nullability differs from the Python-level annotation,
    such as a generated primary key that Target declares not-null but that a not-yet-persisted
    instance must still be constructable without.
    """

    domain: dict[str, Any] = {}
    if primary_key:
        domain["primary_key"] = True
    if auto_increment:
        domain["auto_increment"] = True
    if unique:
        domain["unique"] = True
    if index:
        domain["index"] = True
    if length is not None:
        domain["length"] = length
    if precision is not None:
        domain["precision"] = {"digits": precision[0], "scale": precision[1]}
    if foreign_key is not None:
        domain["foreign_key"] = foreign_key
    if cardinality is not None:
        domain["cardinality"] = cardinality
    if credential is not None:
        domain["credential"] = credential
    if nullable is not None:
        domain["nullable"] = nullable

    return Field(
        default=default,
        description=description,
        json_schema_extra={"domain": domain} if domain else None,
        **kwargs,
    )


def _is_nullable(annotation: Any) -> bool:
    return type(None) in typing.get_args(annotation)


class DomainModel(BaseModel):
    """The technology-independent foundation every concrete Domain Definition shares (Model Principle 4).

    Declares no Field or Domain Relationship of its own; every Domain Definition declares its own
    complete set from the Target.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    persistent: ClassVar[bool] = True
    unique_sets: ClassVar[tuple[tuple[str, ...], ...]] = ()

    @classmethod
    def domain_fields(cls) -> dict[str, dict[str, Any]]:
        """Publish every declared Field's technology-independent vocabulary (Model Principle 9):
        type, length, precision, nullability, default, identity, uniqueness, relationships, and
        credential classification.
        """

        result: dict[str, dict[str, Any]] = {}
        for name, info in cls.model_fields.items():
            extra_raw = info.json_schema_extra
            extra: dict[str, Any] = extra_raw if isinstance(extra_raw, dict) else {}
            domain_raw = extra.get("domain", {})
            metadata: dict[str, Any] = (
                dict(domain_raw) if isinstance(domain_raw, dict) else {}
            )
            metadata.setdefault("nullable", _is_nullable(info.annotation))
            metadata["type"] = info.annotation
            metadata["default"] = (
                None if info.default is PydanticUndefined else info.default
            )
            result[name] = metadata
        return result

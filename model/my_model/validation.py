"""Validation shared by every Model and every consumer.

Consumers reuse this instead of writing their own field checks, so that one
set of rules is applied everywhere. It validates only what a Model's own data
determines. Rules needing application context belong to the layer that runs
the operation, and rules needing stored state — uniqueness across records,
the existence of a referenced record — are guaranteed by the layer that
stores the Model.

Three situations stay distinct throughout:

* **absent** — the field was not supplied. In a complete state it takes its
  declared default or its declared generation; in a partial change it is left
  unchanged.
* **explicitly null** — an attempted value change, valid only where the field
  permits null.
* **pending** — a value awaiting declared generation, marked with ``Pending``.
  It is never replaced by an invented placeholder.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated, Any, get_args, get_origin

from pydantic import ConfigDict, TypeAdapter, ValidationError

from .base import Model, Pending

__all__ = [
    "Change",
    "FieldError",
    "InvalidValue",
    "State",
    "validate_change",
    "validate_state",
]


@dataclass(frozen=True)
class FieldError:
    """One reason a value was refused, naming the field it concerns."""

    field: str
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.field}: {self.message}"


class InvalidValue(Exception):
    """The data does not satisfy what the Model's own declarations require."""

    def __init__(self, model: type[Model], errors: tuple[FieldError, ...]) -> None:
        super().__init__(f"{model.__name__}: " + "; ".join(str(e) for e in errors))
        self.model = model
        self.errors = errors

    @property
    def fields(self) -> tuple[str, ...]:
        return tuple(error.field for error in self.errors)


@dataclass(frozen=True)
class State:
    """A validated complete domain state.

    ``values`` holds every field whose value is known, with defaults applied.
    ``pending`` names the fields awaiting declared generation; they appear in
    neither ``values`` nor the resulting Model until generation supplies them.
    """

    model: type[Model]
    values: dict[str, Any]
    pending: frozenset[str]

    @property
    def is_complete(self) -> bool:
        """No value is still awaiting generation."""
        return not self.pending

    def resolved(self, **generated: Any) -> Model:
        """The Model instance, given a value for each pending field."""
        missing = self.pending - set(generated)
        unexpected = set(generated) - self.pending
        errors = [FieldError(name, "missing", "awaits declared generation") for name in sorted(missing)]
        errors += [FieldError(name, "unknown", "is not awaiting generation") for name in sorted(unexpected)]
        if errors:
            raise InvalidValue(self.model, tuple(errors))
        try:
            return self.model.model_validate({**self.values, **generated})
        except ValidationError as exc:
            raise InvalidValue(self.model, _from_pydantic(exc)) from None


@dataclass(frozen=True)
class Change:
    """A validated partial change.

    ``changes`` holds only the fields whose value is actually changing; an
    omitted field is absent from it and stays as it is. ``pending`` names the
    fields whose new value awaits declared generation.
    """

    model: type[Model]
    changes: dict[str, Any]
    pending: frozenset[str]

    @property
    def is_empty(self) -> bool:
        """Nothing about the record would change."""
        return not self.changes and not self.pending


def validate_state(model: type[Model], data: Mapping[str, Any]) -> State:
    """Validate a complete domain state.

    An absent field takes its declared default, or its declared generation,
    or is refused as missing. An explicit null is accepted only where the
    field permits null. A field marked ``Pending`` is recorded as pending.
    """
    specs = model.field_specs()
    errors: list[FieldError] = []
    values: dict[str, Any] = {}
    pending: set[str] = set()

    for name in data:
        if name not in specs:
            errors.append(FieldError(name, "unknown", "the Model declares no such field"))

    for name, spec in specs.items():
        if name in data:
            given = data[name]
            if given is Pending:
                if spec.generated:
                    pending.add(name)
                else:
                    errors.append(FieldError(name, "generation_not_permitted",
                                             "does not permit a generated value"))
            elif given is None:
                if spec.nullable:
                    values[name] = None
                else:
                    errors.append(FieldError(name, "not_null", "does not permit a null value"))
            else:
                _apply(model, name, given, values, errors)
            continue
        if spec.has_default:
            values[name] = spec.default
        elif spec.generated:
            pending.add(name)
        elif spec.nullable:
            values[name] = None
        elif spec.assigned_by_storage:
            values[name] = None
        else:
            errors.append(FieldError(name, "missing",
                                     "is required and has no default and no declared generation"))

    if errors:
        raise InvalidValue(model, tuple(errors))
    return State(model, values, frozenset(pending))


def validate_change(model: type[Model], data: Mapping[str, Any]) -> Change:
    """Validate a partial change.

    Only the supplied fields are considered; every omitted field stays
    unchanged. An explicit null is accepted only where the field permits
    null, and a field marked ``Pending`` is recorded as pending.
    """
    specs = model.field_specs()
    errors: list[FieldError] = []
    changes: dict[str, Any] = {}
    pending: set[str] = set()

    for name, given in data.items():
        spec = specs.get(name)
        if spec is None:
            errors.append(FieldError(name, "unknown", "the Model declares no such field"))
        elif spec.assigned_by_storage:
            errors.append(FieldError(name, "immutable", "is assigned by the storing layer"))
        elif given is Pending:
            if spec.generated:
                pending.add(name)
            else:
                errors.append(FieldError(name, "generation_not_permitted",
                                         "does not permit a generated value"))
        elif given is None:
            if spec.nullable:
                changes[name] = None
            else:
                errors.append(FieldError(name, "not_null", "does not permit a null value"))
        else:
            _apply(model, name, given, changes, errors)

    if errors:
        raise InvalidValue(model, tuple(errors))
    return Change(model, changes, frozenset(pending))


# ---------------------------------------------------------------------------
# internals
# ---------------------------------------------------------------------------


def _apply(model: type[Model], name: str, given: Any, into: dict[str, Any],
           errors: list[FieldError]) -> None:
    try:
        into[name] = _adapter(model, name).validate_python(given)
    except ValidationError as exc:
        errors.append(FieldError(name, "invalid", exc.errors()[0]["msg"]))


@lru_cache(maxsize=None)
def _adapter(model: type[Model], name: str) -> TypeAdapter:
    """A strict validator for one field, carrying its declared constraints."""
    info = model.model_fields[name]
    annotation = _non_null(info.annotation)
    if info.metadata:
        annotation = Annotated[(annotation, *info.metadata)]
    return TypeAdapter(annotation, config=ConfigDict(strict=True))


def _non_null(annotation: Any) -> Any:
    if get_origin(annotation) is not None:
        args = [a for a in get_args(annotation) if a is not type(None)]
        if len(args) == 1:
            return args[0]
    return annotation


def _from_pydantic(exc: ValidationError) -> tuple[FieldError, ...]:
    return tuple(
        FieldError(".".join(str(p) for p in error["loc"]) or "?", "invalid", error["msg"])
        for error in exc.errors()
    )

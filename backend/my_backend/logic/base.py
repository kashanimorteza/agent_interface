"""What every kind of data can do, before any of them does anything different.

The operations here are the ones every kind of data shares. A unit inherits
them, and the moment one kind needs its own rule it overrides exactly that and
leaves the rest alone.

Nothing in here knows how a request arrived or how a record is held. It knows
what the application does and what has to be true for it to do it.
"""

from __future__ import annotations

from typing import Any, ClassVar, Mapping

from my_model import Entity, PartialView, is_stated
from pydantic import ValidationError

from ..data_access import DataAccess, Operations
from ..faults import Invalid, NotFound, Unsupported

STATUS_FIELD = "status"


class ModelLogic:
    """The behaviour one kind of data has, and the baseline all of them share."""

    definition: ClassVar[type[Entity]]

    def __init__(self, data: DataAccess) -> None:
        self._data = data

    # <!---------------------------- what this kind of data is -->

    @property
    def name(self) -> str:
        return self.definition.entity_name

    @classmethod
    def key_field(cls) -> str:
        """The field that identifies one record of this kind."""

        for field_name, spec in cls.definition.entity_fields.items():
            if is_stated(spec.primary_key) and spec.primary_key:
                return field_name
        raise Unsupported(f"{cls.definition.entity_name} has nothing that identifies a record")

    @classmethod
    def offers_status(cls) -> bool:
        """Whether this kind of data has somewhere to put an enabled state."""

        return STATUS_FIELD in cls.definition.entity_fields

    # <!---------------------------- the shared baseline -->

    def create(self, values: Mapping[str, Any]) -> PartialView:
        """Bring one record of this kind into being."""

        self.check(dict(values), existing=None)
        with self._data.unit() as unit:
            return unit.create(self.definition, dict(values))

    def get(self, identifier: Any) -> PartialView:
        """One record of this kind, or a refusal saying it is not there."""

        with self._data.unit() as unit:
            found = unit.get(self.definition, {self.key_field(): identifier})
        if found is None:
            raise NotFound(f"no {self.name} has {self.key_field()} {identifier!r}")
        return found

    def list(
        self,
        criteria: Mapping[str, Any] | None = None,
        *,
        limit: int | None = None,
        offset: int | None = None,
        order_by: str | None = None,
    ) -> list[PartialView]:
        """The records of this kind that match."""

        with self._data.unit() as unit:
            return unit.list(
                self.definition, criteria, limit=limit, offset=offset, order_by=order_by
            )

    def update(self, identifier: Any, changes: Mapping[str, Any]) -> PartialView:
        """Change the stated fields of one record, and no others."""

        criteria = {self.key_field(): identifier}
        with self._data.unit() as unit:
            existing = unit.get(self.definition, criteria)
            if existing is None:
                raise NotFound(f"no {self.name} has {self.key_field()} {identifier!r}")

            self.check(dict(changes), existing=existing)
            unit.update(self.definition, criteria, dict(changes))
            changed = unit.get(self.definition, criteria)

        if changed is None:  # pragma: no cover - it was just read in the same unit
            raise NotFound(f"no {self.name} has {self.key_field()} {identifier!r}")
        return changed

    def delete(self, identifier: Any) -> None:
        """Remove one record of this kind."""

        criteria = {self.key_field(): identifier}
        with self._data.unit() as unit:
            if unit.get(self.definition, criteria) is None:
                raise NotFound(f"no {self.name} has {self.key_field()} {identifier!r}")
            unit.delete(self.definition, criteria)

    def set_status(self, identifier: Any, *, enabled: bool) -> PartialView:
        """Enable or disable one record, where this kind of data allows it."""

        if not self.offers_status():
            raise Unsupported(
                f"{self.name} declares no {STATUS_FIELD} field, so it cannot be "
                f"enabled or disabled"
            )
        criteria = {self.key_field(): identifier}
        with self._data.unit() as unit:
            if unit.get(self.definition, criteria) is None:
                raise NotFound(f"no {self.name} has {self.key_field()} {identifier!r}")
            unit.set_status(self.definition, criteria, enabled=enabled)
            changed = unit.get(self.definition, criteria)
        return changed

    # <!---------------------------- what has to be true -->

    def check(self, values: Mapping[str, Any], *, existing: PartialView | None) -> None:
        """Judge the state an operation would produce, not the values it carries.

        A change stating one field still has to leave a whole record that the
        definition would accept, so what is already stored is read back and the
        two are judged together. What only stored records can settle is left to
        the layer that holds them.
        """

        resulting = dict(existing.stated_fields()) if existing is not None else {}
        resulting.update({name: value for name, value in values.items()})

        unknown = set(resulting) - set(self.definition.entity_fields)
        if unknown:
            raise Invalid(f"{self.name} has no field {sorted(unknown)}")

        # Fields the record carries but this layer never sees back — a
        # credential among them — are not missing, only invisible from here.
        withheld = {
            name: "withheld"
            for name, spec in self.definition.entity_fields.items()
            if name not in resulting and spec.is_required_in_state() and existing is not None
        }

        try:
            self.definition(**{**resulting, **withheld})
        except ValidationError as error:
            raise Invalid(_readable(error)) from error

        self.check_context(resulting, existing=existing)

    def check_context(self, resulting: Mapping[str, Any], *, existing: PartialView | None) -> None:
        """Conditions this kind of data adds beyond what its values say.

        Nothing by default: a kind of data with a rule of its own overrides
        this, and only that kind is affected.
        """


def _readable(error: ValidationError) -> str:
    """A validation refusal said plainly, carrying no value that was rejected."""

    parts = []
    for problem in error.errors():
        where = ".".join(str(piece) for piece in problem["loc"]) or "the record"
        parts.append(f"{where}: {problem['msg']}")
    return "; ".join(parts)


__all__ = ["ModelLogic", "STATUS_FIELD"]

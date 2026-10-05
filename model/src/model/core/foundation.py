import json
from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation
from typing import Any, ClassVar, Self
from uuid import UUID

from model.core.declaration import Declaration, FieldDeclaration, FieldType
from model.core.errors import EntityValidationError


def _encode(field: FieldDeclaration, value: Any) -> Any:
    if value is None:
        return None
    match field.type:
        case FieldType.DECIMAL:
            return str(value)
        case FieldType.DATETIME | FieldType.DATE | FieldType.TIME:
            return value.isoformat()
        case FieldType.UUID:
            return str(value)
        case _:
            return value


def _decode(entity: str, field: FieldDeclaration, value: Any) -> Any:
    if value is None:
        return None
    problem = f"{entity}: field '{field.name}': JSON value does not match Type '{field.type}'."
    if field.type in (
        FieldType.DECIMAL,
        FieldType.DATETIME,
        FieldType.DATE,
        FieldType.TIME,
        FieldType.UUID,
    ) and not isinstance(value, str):
        raise EntityValidationError(problem)
    try:
        match field.type:
            case FieldType.DECIMAL:
                decoded = Decimal(value)
                if not decoded.is_finite():
                    raise ValueError
                return decoded
            case FieldType.DATETIME:
                return datetime.fromisoformat(value)
            case FieldType.DATE:
                return date.fromisoformat(value)
            case FieldType.TIME:
                return time.fromisoformat(value)
            case FieldType.UUID:
                return UUID(value)
            case FieldType.FLOAT if isinstance(value, int) and not isinstance(
                value, bool
            ):
                return float(value)
            case _:
                return value
    except InvalidOperation, ValueError, OverflowError:
        raise EntityValidationError(problem) from None


def _reject_constant(name: str) -> Any:
    raise ValueError(f"Non-standard JSON constant '{name}'.")


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key '{key}'.")
        result[key] = value
    return result


class Foundation:
    declaration: ClassVar[Declaration]

    @classmethod
    def _reconstruct(cls, values: dict[str, Any]) -> Self:
        raise NotImplementedError

    def to_json(self) -> str:
        values = {
            field.name: _encode(field, getattr(self, field.name))
            for field in self.declaration.fields
        }
        return json.dumps(values, allow_nan=False)

    @classmethod
    def from_json(cls, text: str) -> Self:
        name = cls.declaration.name
        if not isinstance(text, str):
            raise EntityValidationError(f"{name}: JSON text must be a string.")
        try:
            document = json.loads(
                text,
                parse_constant=_reject_constant,
                object_pairs_hook=_reject_duplicates,
            )
        except ValueError as error:
            raise EntityValidationError(
                f"{name}: malformed JSON text ({error})."
            ) from None
        if not isinstance(document, dict):
            raise EntityValidationError(f"{name}: JSON root must be an object.")
        fields = {field.name: field for field in cls.declaration.fields}
        values = {
            key: _decode(name, fields[key], value) if key in fields else value
            for key, value in document.items()
        }
        return cls._reconstruct(values)

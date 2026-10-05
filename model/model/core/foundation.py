import json
from typing import Any, ClassVar, NoReturn, Self

from pydantic import BaseModel, ValidationError

from model.core._fields import adapter, declared, entity_error, retarget
from model.core.declaration import Declaration


def _reject_constant(constant: str) -> NoReturn:
    raise ValueError("JSON text must conform to the JSON standard")


class Foundation(BaseModel):
    declaration: ClassVar[Declaration]

    def to_json(self) -> str:
        values = self.model_dump(mode="json")
        return json.dumps({name: values[name] for name in type(self).model_fields}, separators=(",", ":"))

    @classmethod
    def from_json(cls, text: str) -> Self:
        try:
            parsed = json.loads(text, parse_constant=_reject_constant)
        except ValueError:
            raise ValueError("Text is not valid JSON") from None
        if not isinstance(parsed, dict):
            raise ValueError("JSON text must have one object at its root")
        values: dict[str, Any] = {}
        failures: list[Any] = []
        for name, value in parsed.items():
            if name not in cls.model_fields:
                failures.append({"type": "extra_forbidden", "loc": (name,), "input": None})
                continue
            if declared(cls)[name].type == "decimal" and value is not None and not isinstance(value, str):
                failures.append({"type": "string_type", "loc": (name,), "input": None})
                continue
            try:
                values[name] = adapter(cls, name).validate_json(json.dumps(value), strict=True)  # type: ignore[arg-type]
            except ValidationError as error:
                failures.extend(retarget(error, name))
        if failures:
            raise entity_error(cls, failures)
        return cls.model_validate(values, strict=True)

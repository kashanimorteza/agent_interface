import keyword
from decimal import Decimal
from typing import Any

from sqlalchemy import Identity, Index, String, TypeDecorator, UniqueConstraint
from sqlalchemy.engine import Dialect
from sqlmodel import Field

from model.core.declaration import Declaration, FieldType, ValueGeneration


class DecimalText(TypeDecorator[Decimal]):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: Decimal | None, dialect: Dialect) -> str | None:
        return None if value is None else str(value)

    def process_result_value(
        self, value: str | None, dialect: Dialect
    ) -> Decimal | None:
        return None if value is None else Decimal(value)


def physical_name(logical: str) -> str:
    name = "".join(word[:1].upper() + word[1:] for word in logical.split())
    if not name.isidentifier() or keyword.iskeyword(name):
        raise ValueError(f"Entity '{logical}': no valid physical name can be derived.")
    return name


def column(declaration: Declaration, name: str) -> Any:
    field = next(item for item in declaration.fields if item.name == name)
    options: dict[str, Any] = {"description": field.description}
    if field.has_default:
        options["default"] = field.default
    elif field.value_generation is ValueGeneration.AUTO_INCREMENT or field.nullable:
        options["default"] = None
    if field.constraints.size is not None:
        options["max_length"] = field.constraints.size
    if name == declaration.primary_key:
        options["primary_key"] = True
    if any(item.fields == (name,) for item in declaration.unique_constraints):
        options["unique"] = True
    if any(item.fields == (name,) for item in declaration.indexes):
        options["index"] = True
    for relation in declaration.relations:
        if relation.local_field == name:
            target = physical_name(relation.target_entity)
            options["foreign_key"] = f"{target}.{relation.target_field}"
    if field.value_generation is ValueGeneration.AUTO_INCREMENT:
        options["sa_column_args"] = [Identity()]
    if field.type is FieldType.DECIMAL:
        options["sa_type"] = DecimalText
    return Field(**options)


def table_arguments(declaration: Declaration) -> tuple[Any, ...]:
    constructs: list[Any] = [
        UniqueConstraint(*item.fields)
        for item in declaration.unique_constraints
        if len(item.fields) > 1
    ]
    constructs += [
        Index(None, *item.fields)
        for item in declaration.indexes
        if len(item.fields) > 1
    ]
    options: dict[str, Any] = {}
    if any(
        item.value_generation is ValueGeneration.AUTO_INCREMENT
        for item in declaration.fields
    ):
        options["sqlite_autoincrement"] = True
    return (*constructs, options)

"""The Account Group Adapter: the Endpoints of the Account Group Entity."""

from typing import Annotated, Any

from fastapi import APIRouter, Body, Path, Query
from logic.interface import Entity
from pydantic import AfterValidator

from api.conversion import (
    Combination,
    FilterList,
    Instance,
    OrderList,
    to_entity,
    to_field,
    to_filters,
    to_orders,
)

model = Entity.Model.AccountGroup
service = Entity.Service.AccountGroup()

router = APIRouter(prefix="/account_group", tags=["Entity · AccountGroup"])


@router.post("/add")
def add(
    entity: Annotated[
        dict[str, Any], Body(embed=True), AfterValidator(to_entity(model))
    ],
    instance: Annotated[Instance, Body(embed=True)] = None,
):
    """Store one new Entity instance and return the stored Entity, including generated values."""
    return service.add(entity, instance)


@router.put("/update")
def update(
    entity: Annotated[
        dict[str, Any], Body(embed=True), AfterValidator(to_entity(model))
    ],
    instance: Annotated[Instance, Body(embed=True)] = None,
):
    """Replace every mutable Field of the stored record of an Entity instance; None when it does not exist."""
    return service.update(entity, instance)


@router.post("/list")
def list(
    filters: Annotated[
        FilterList | None, Body(embed=True), AfterValidator(to_filters(model))
    ] = None,
    combination: Annotated[Combination, Body(embed=True)] = None,
    orders: Annotated[
        OrderList | None, Body(embed=True), AfterValidator(to_orders(model))
    ] = None,
    limit: Annotated[int | None, Body(embed=True)] = None,
    instance: Annotated[Instance, Body(embed=True)] = None,
):
    """Return the matching Entity instances; a zero or negative limit means no limit."""
    return service.list(filters, combination, orders, limit, instance)


@router.get("/get_by_id/{id}")
def get_by_id(
    id: Annotated[int, Path()],
    instance: Annotated[Instance, Query()] = None,
):
    """Return the Entity with that id, or None when no record exists."""
    return service.get_by_id(id, instance)


@router.delete("/delete/{id}")
def delete(
    id: Annotated[int, Path()],
    instance: Annotated[Instance, Query()] = None,
):
    """Remove the record and return the deleted Entity, or None when no record exists."""
    return service.delete(id, instance)


@router.patch("/enable/{id}")
def enable(
    id: Annotated[int, Path()],
    instance: Annotated[Instance, Body(embed=True)] = None,
):
    """Set only is_active to true and return the final Entity, or None when no record exists."""
    return service.enable(id, instance)


@router.patch("/disable/{id}")
def disable(
    id: Annotated[int, Path()],
    instance: Annotated[Instance, Body(embed=True)] = None,
):
    """Set only is_active to false and return the final Entity, or None when no record exists."""
    return service.disable(id, instance)


@router.post("/count")
def count(
    filters: Annotated[
        FilterList | None, Body(embed=True), AfterValidator(to_filters(model))
    ] = None,
    combination: Annotated[Combination, Body(embed=True)] = None,
    instance: Annotated[Instance, Body(embed=True)] = None,
):
    """Return the number of matching records."""
    return service.count(filters, combination, instance)


@router.post("/sum")
def sum(
    field: Annotated[str, Body(embed=True), AfterValidator(to_field(model))],
    filters: Annotated[
        FilterList | None, Body(embed=True), AfterValidator(to_filters(model))
    ] = None,
    combination: Annotated[Combination, Body(embed=True)] = None,
    instance: Annotated[Instance, Body(embed=True)] = None,
):
    """Return the total of a numeric Field, ignoring null values, or zero when nothing matches."""
    return service.sum(field, filters, combination, instance)


@router.post("/min")
def min(
    field: Annotated[str, Body(embed=True), AfterValidator(to_field(model))],
    filters: Annotated[
        FilterList | None, Body(embed=True), AfterValidator(to_filters(model))
    ] = None,
    combination: Annotated[Combination, Body(embed=True)] = None,
    instance: Annotated[Instance, Body(embed=True)] = None,
):
    """Return the smallest non-null value of a comparable Field, or None when nothing matches."""
    return service.min(field, filters, combination, instance)


@router.post("/max")
def max(
    field: Annotated[str, Body(embed=True), AfterValidator(to_field(model))],
    filters: Annotated[
        FilterList | None, Body(embed=True), AfterValidator(to_filters(model))
    ] = None,
    combination: Annotated[Combination, Body(embed=True)] = None,
    instance: Annotated[Instance, Body(embed=True)] = None,
):
    """Return the largest non-null value of a comparable Field, or None when nothing matches."""
    return service.max(field, filters, combination, instance)


@router.delete("/truncate")
def truncate(
    instance: Annotated[Instance, Query()] = None,
):
    """Remove every record of the Entity, keep its Table, and return the deleted count."""
    return service.truncate(instance)

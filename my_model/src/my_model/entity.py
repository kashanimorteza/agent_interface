"""A domain-neutral example Model.

This Model exists solely to keep this package's README usage examples
runnable while staying domain-neutral. It is NOT part of the project's
domain Model set defined by the current Target, and no other Model in this
package depends on it.
"""

from pydantic import Field

from ._base import BaseModel, credential_field
from .types import Percentage


class Entity(BaseModel):
    """A domain-neutral placeholder Model, used only in README usage examples."""

    id: int | None = Field(default=None, description="The entity's generated identity.")
    name: str = Field(description="The entity's display name.")
    owner_id: int = Field(
        description="Illustrates a declared relationship: this entity belongs to one owner."
    )
    weight: Percentage = Field(
        description="Illustrates a reusable domain type: a percentage between 0 and 100."
    )
    secret: str = credential_field(
        storage="hash", description="Illustrates a credential field's declared storage-at-rest meaning."
    )
    status: bool = Field(default=True, description="Indicates whether the entity is active.")
    description: str | None = Field(default=None, description="Describes the entity.")

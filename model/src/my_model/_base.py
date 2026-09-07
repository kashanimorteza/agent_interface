"""The shared base class of every logical Model."""

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    """Base of every shared Model.

    Construction validates field types, nullability, and defaults; an unknown
    field is rejected; assignments are validated. The primary key and credential
    fields may be absent on an instance: persistence assigns the key on create and
    credential values are write-only, never returned.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True, from_attributes=True)

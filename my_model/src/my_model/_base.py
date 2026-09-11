from pydantic import BaseModel as _PydanticBaseModel
from pydantic import ConfigDict


class BaseModel(_PydanticBaseModel):
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

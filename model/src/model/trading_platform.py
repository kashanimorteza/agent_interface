"""The TradingPlatform Domain Definition.

A supported trading API standard, independent of any exchange or broker.

Choices where the Target is silent: declared persistent, because the Target gives the concept a
generated identity and stored records; `id` has no value until it is produced; text Fields carry
no length bound unless the Target states one; a nullable Field has no default and must be
supplied explicitly.
"""

from typing import Annotated

from model.declaration import Activation, Generated, Identity, Persistence, Unique
from model.foundation import ModelFoundation


class TradingPlatform(ModelFoundation):
    persistence = Persistence.PERSISTENT

    id: Annotated[int | None, Identity(), Generated()] = None
    name: Annotated[str, Unique()]
    code: str
    is_active: Annotated[bool, Activation()] = True
    description: str | None

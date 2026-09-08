"""The application layer of Trading Assistant.

This layer is what the application *does*. It takes the domain definitions the
Model layer publishes, keeps the rules that depend on an operation rather than
on values alone, reaches stored data only through the persistence layer's
published boundary, and offers the result as one contract over the resolved
transport.

What it publishes to anything outside itself:

* ``create_app`` — build the application from the settings and bindings it is
  given, and ``app``, one built from the ones it was given here.
* the refusals a caller can meet, so a consumer in the same process can tell one
  kind of refusal from another.

What it does not publish: the units of behaviour, the route to stored data, and
the shapes the contract carries. Those are how the contract is kept, and the
contract is what anyone outside should be depending on.
"""

from .api import app, create_app
from .configuration import Configuration, load
from .faults import (
    BackendFault,
    Conflict,
    Invalid,
    Misconfigured,
    NotFound,
    Unsupported,
)

__version__ = "0.1.0"

__all__ = [
    "BackendFault",
    "Configuration",
    "Conflict",
    "Invalid",
    "Misconfigured",
    "NotFound",
    "Unsupported",
    "app",
    "create_app",
    "load",
    "__version__",
]

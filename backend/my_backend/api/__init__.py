"""API — the external boundary of this layer.

The top of the three responsibilities here, and the only one anything outside
the layer meets. It decodes what arrives, calls the behaviour that answers it,
turns the result into a response, and describes the whole contract. It reaches
the behaviour below it and nothing beneath that.
"""

from .app import app, create_app
from .representations import Shapes
from .routes import resource_path

__all__ = ["Shapes", "app", "create_app", "resource_path"]

"""Logic — what the application does.

The middle of the three responsibilities in this layer. Every kind of data the
project defines has its own unit here, sharing a common baseline; each judges
what its operations require, and reaches stored data only through the
responsibility below. Nothing here knows how a request arrived.
"""

from .base import ModelLogic
from .registry import UNITS, Behaviour

__all__ = ["UNITS", "Behaviour", "ModelLogic"]

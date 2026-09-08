"""Data Access — the only Backend boundary that reaches stored data.

The lowest of the three responsibilities in this layer. It turns the data
operations asked for above into calls on what the persistence layer publishes,
and turns what comes back into logical data. Nothing above it reaches stored
data by any other route, and nothing of how that data is held travels upward.
"""

from .gateway import DataAccess, Operations

__all__ = ["DataAccess", "Operations"]

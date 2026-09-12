"""The public Instance Registry.

Canonical usage::

    import my_database
    my_database.instances.registry.list()
"""

from my_database._registry import InstanceIdentity
from my_database._registry import instances as registry

__all__ = ["InstanceIdentity", "registry"]

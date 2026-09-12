"""Public interface of the my_database package.

    import my_database
    my_database.interface.add(my_model.user.User(...))

Consumers reach persistence only through `interface` (data operations and
transactions) and `registry` (Instance discovery). No other module in this
package is part of the public contract.
"""

from my_database import interface, registry

__all__ = ["interface", "registry"]

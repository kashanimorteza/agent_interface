"""The public transaction boundary.

Canonical usage::

    import my_database
    with my_database.transactions.transaction() as session:
        ...
"""

from my_database._transactions import transaction

__all__ = ["transaction"]

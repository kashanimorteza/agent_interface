"""Public initial-data seeding utility.

Canonical usage::

    import my_database
    my_database.seeding.seed_initial_data()
"""

from my_database._seed import seed_initial_data

__all__ = ["seed_initial_data"]

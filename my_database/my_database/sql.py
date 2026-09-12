"""The public controlled SQL execution route.

Canonical usage::

    import my_database
    my_database.sql.execute_controlled_sql(sql, params, table="currencies")
"""

from my_database._sql import ALLOWED_TABLES, execute_controlled_sql

__all__ = ["ALLOWED_TABLES", "execute_controlled_sql"]

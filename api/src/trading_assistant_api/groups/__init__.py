"""Groups: exactly one per eligible Logic Service, each with its own Router and Adapter.

Each Group is generated from a Service whose `publish_in_logic_interface` and `generate_api`
settings, read from Logic's Service Preferences, are both true. Today that is Entity Service
alone; Storage Service, which enables neither, has none.
"""

from trading_assistant_api.groups import entity

GROUPS = (entity,)

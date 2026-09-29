"""Collection bounds: the page size every collection Endpoint applies.

The values are the API Preferences' pagination settings. Logic's list Action accepts a `limit`
and reads zero or less as no limit, so a request always reaches Logic with a limit between one
and the maximum.
"""

DEFAULT_LIMIT = 50
MAXIMUM_LIMIT = 100

"""The error every invalid Logic configuration is reported through."""


class ConfigurationError(ValueError):
    """A configured value of Logic is invalid, so nothing is published."""

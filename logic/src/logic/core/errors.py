"""Errors Logic raises for its own declarations and configuration."""


class ConfigurationError(ValueError):
    """A Logic declaration or required configuration value is missing or invalid."""


class EntityMismatchError(TypeError):
    """An Entity instance does not belong to the Child Service it was given to."""

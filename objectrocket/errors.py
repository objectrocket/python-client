"""Exceptions raised by the ObjectRocket Python client."""


class ObjectRocketException(Exception):
    """Base class for all ObjectRocket exceptions."""
    pass


class InstancesException(ObjectRocketException):
    """Exception for instances layer operations."""
    pass


class AuthFailure(ObjectRocketException):
    """Raised when a requst's response code is 401."""
    pass

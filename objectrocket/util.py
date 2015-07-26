"""Utility code for the objectrocket package."""
import functools
import types

from objectrocket import errors


def register_extension_class(ext, base, *args, **kwargs):
    """Instantiate the given extension class and register as a public attribute of the given base.

    README: The expected protocol here is to instantiate the given extension and pass the base
    object as the first positional argument, then unpack args and kwargs as additional arguments to
    the extension's constructor.
    """
    ext_instance = ext.plugin(base, *args, **kwargs)
    setattr(base, ext.name.lstrip('_'), ext_instance)


def register_extension_method(ext, base, *args, **kwargs):
    """Register the given extension method as a public attribute of the given base.

    README: The expected protocol here is that the given extension method is an unbound function.
    It will be bound to the specified base as a method, and then set as a public attribute of that
    base.
    """
    bound_method = types.MethodType(ext.plugin, base, base.__class__)
    setattr(base, ext.name.lstrip('_'), bound_method)


def token_auto_auth(func):
    """Wrap class methods with automatic token re-authentication.

    This wrapper will detect authentication failures coming from its wrapped method. When one is
    caught, it will request a new token, and simply replay the original request.

    The one constraint that this wrapper has is that the wrapped method's class must have the
    :py:class:`objectrocket.client.Client` object embedded in it as the property ``_client``. Such
    is the design of all current client operations layers.
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            response = func(self, *args, **kwargs)

        # If auth failure occurs, attempt to re-authenticate and replay once at most.
        except errors.AuthFailure:

            # Request to have authentication refreshed.
            self._client.auth._refresh()

            # Replay original request.
            response = func(self, *args, **kwargs)

        return response

    # TODO(TheDodd): match func call signature and docs.
    return wrapper

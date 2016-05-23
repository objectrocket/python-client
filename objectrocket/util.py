"""Utility code for the objectrocket package."""
import functools
import datetime

from six import create_bound_method

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
    bound_method = create_bound_method(ext.plugin, base)
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


def sum_values(value1, value2):
    # function borrowed from core, keeping original comment intact
    # TODO: Kill this method with fire, it's the only way to be sure
    if value1 is None:
        return value2
    if value2 is None:
        return value1

    number_types = (int, float, long, bool)

    if isinstance(value1, number_types) and isinstance(value2, number_types):
        return int(value1 + value2)

    # make sure the entries are of the same type
    if not (isinstance(value1, value2.__class__) or isinstance(value2, value1.__class__)):
        message = ("Entry %s type %s and entry %s type %s are not of the same type"
                   % (str(value1), str(type(value1)), str(value2), str(type(value2))))
        raise TypeError(message)

    if isinstance(value1, list):
        return list(set(value1 + value2))
    elif isinstance(value1, str) or isinstance(value1, datetime.datetime) or isinstance(value1, unicode):
        return value1
    elif isinstance(value1, dict):
        keys = set(value1.iterkeys()) | set(value2.iterkeys())
        return dict((key, sum_values(value1.get(key), value2.get(key))) for key in keys)
    else:
        return value1 + value2

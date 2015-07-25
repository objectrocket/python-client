"""Utility code for the objectrocket package."""
import types


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

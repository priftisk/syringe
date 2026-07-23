import inspect
from syringe.registry.router import register_route

def route(path, methods=["GET"]):
    def decorator(fn_or_view):
        allowed_methods = methods
        if inspect.isclass(fn_or_view):
            allowed_methods = getattr(
                fn_or_view, "_allowed_methods"
            )  # _allowed_methods is injected from the View class
        register_route(allowed_methods, path, fn_or_view)
        return fn_or_view

    return decorator


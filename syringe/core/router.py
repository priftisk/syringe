import inspect
from syringe.registry.router import register_route, get_route_handler

def route(path, methods=["GET"]):
    def decorator(fn):
        allowed_methods = methods
        if inspect.isclass(fn):
            allowed_methods = getattr(
                fn, "_allowed_methods"
            )  # _allowed_methods is injected from the View class
        register_route(allowed_methods, path, fn)
        return fn

    return decorator


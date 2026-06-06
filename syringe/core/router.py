import inspect
from syringe.views.base import View
from syringe.registry.router import register_route, get_route


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


def resolve_handler(request):
    target = get_route(request)

    if target is None:
        return None

    if inspect.isclass(target) and issubclass(target, View):  # If View class

        def handler(req):
            view = target()
            response = view.dispatch(req)
            return response

        return handler

    return target

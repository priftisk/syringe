import inspect
from syringe.views.base import View
from syringe.registry.router import register_route, get_route


def route(path, methods=["GET"]):
    def decorator(fn):

        if inspect.isclass(fn):
            for method in getattr(
                fn, "_allowed_methods", []
            ):  # _allowed_methods is injected from the View class
                register_route(method, path, fn)
        else:
            for method in methods:
                register_route(method, path, fn)

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

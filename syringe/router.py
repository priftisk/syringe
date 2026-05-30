import inspect
from views import View
from .response import Response


class Router:
    def __init__(self):
        self._routes = {}

    def route(self, path, methods=["GET"]):
        def decorator(fn):
            # fn may be a function OR a View subclass — store either
            if inspect.isclass(fn):
                # register for every method the view supports
                for method in fn._allowed_methods:
                    self._routes[f"{method} {path}"] = fn
            else:
                for method in methods:
                    self._routes[f"{method} {path}"] = fn
            return fn

        return decorator

    def resolve(self, request):
        target = self._routes.get(f"{request.method} {request.path}")

        if target is None:
            return None

        if inspect.isclass(target):

            def handler(req):
                view = target()
                response = view.dispatch(req)
                return response

            return handler

        return target

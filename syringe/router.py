import inspect


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

    def resolve(self, method, path):
        path = path.split("?")[0]  # strip query string
        target = self._routes.get(f"{method} {path}")
        if target is None:
            return None
        if inspect.isclass(target):
            # instantiate and dispatch — one new instance per request
            body, status = target().dispatch(method)
            return lambda: (body, status)

        return lambda: (target, 200)

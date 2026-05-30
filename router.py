class Router:
    def __init__(self):
        self._routes = {}

    def route(self, path, methods=["GET"]):
        def decorator(fn):
            for method in methods:
                self._routes[f"{method} {path}"] = fn
            return fn

        return decorator

    def resolve(self, method, path):
        return self._routes.get(f"{method} {path}")

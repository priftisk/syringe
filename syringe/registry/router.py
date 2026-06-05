class Router:
    _registry = {}


def register_route(method, path, handler):
    Router._registry[f"{method} {path}"] = handler
    print(f"Registered: {method} {path}")


def get_route(request):
    return Router._registry.get(f"{request.method} {request.path}", None)

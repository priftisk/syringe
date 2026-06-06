from syringe.core.route import Route
from syringe.core.request import Request
import inspect


class Router:
    _registry = {}


def register_route(method, path, handler):
    new_route = Route(method, path)
    if (
        inspect.isclass(handler) and new_route.base_path in Router._registry
    ):  # is View and already registered entire class
        return

    Router._registry.setdefault(new_route.base_path, []).append((new_route, handler))
    print(f"Registered: {new_route.method} {new_route.base_path}")


def get_route(request):
    base_match = Router._registry.get(request.path.base, None)
    if not base_match:
        return None
    for route, handler in base_match:
        if _match(route, request):
            return handler
    return None


def _match(route: Route, request: Request):
    if len(route.params) == len(request.path._params_list):
        request.path._set_params(
            route.params
        )  # Inject route params into path, so it constructs the path params for the request
        return True
    return False

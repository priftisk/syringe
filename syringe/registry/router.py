from syringe.core.route import Route
from syringe.views.base import View
from syringe.util.core import params_match, methods_match
import inspect


class Router:
    _registry = {}


def register_route(methods, path, handler):
    is_view = inspect.isclass(handler) and issubclass(handler, View)

    new_route = Route(methods, path)
    if (
        is_view and new_route.base_path in Router._registry
    ):  # is View and already registered entire class
        return

    Router._registry.setdefault(new_route.base_path, []).append((new_route, handler))
    print(f"Registered: {new_route.methods} {new_route.base_path}")


def get_route(request):
    base_path_match = Router._registry.get(request.path.base, None)
    if not base_path_match:
        return None
    for route, handler in base_path_match:
        if not methods_match(route, request):
            continue
        if params_match(
            route, request
        ):  # Found matching base path with matching path params
            request.path._set_params(
                route.params
            )  # Inject route params into path, so it constructs the path params dict for the request
            return handler
    return None

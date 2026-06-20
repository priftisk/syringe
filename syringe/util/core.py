
STATUS_TEXT = {
    200: "OK",
    201: "Created",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
}

def get_local_ip():
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create udp socket
        s.connect(("8.8.8.8", 80))  # doesn't actually send data
        ip = s.getsockname()[0] # See which ip was assigned by the OS to connect
        s.close()
        return ip
    except Exception:
        return "0.0.0.0"

def methods_match(route, request):
    return request.method.upper() in route.methods


def params_match(route, request): #TODO deeper check
    return len(route.params) == len(request.path._params_list)


def apply_middlewares(handler, middlewares):
    for mw in reversed(middlewares):
        handler = mw(handler)
    return handler


def autodiscover(package_name):
    import importlib, pkgutil

    package = importlib.import_module(package_name)
    # print(package)

    for _, module_name, _ in pkgutil.walk_packages(
        package.__path__, package.__name__ + "."
    ):
        importlib.import_module(module_name)

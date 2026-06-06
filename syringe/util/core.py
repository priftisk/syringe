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

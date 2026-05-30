from functools import wraps
from .request import Request
from .response import Response
import time


def not_found_middleware(handler):
    @wraps(handler)
    def wrapper(request):
        if handler is None:
            return Response("<h1>404 Not Found</h1>", 404)
        return handler(request)

    return wrapper


def logging_middleware(handler):
    @wraps(handler)
    def wrapper(request: Request):

        start = time.perf_counter()
        response: Response = handler(request)
        elapsed = time.perf_counter() - start
        print(
            f"{request.method} {request.path} -> {response.status} [{(elapsed * 1000):.5f}ms]"
        )

        return response

    return wrapper

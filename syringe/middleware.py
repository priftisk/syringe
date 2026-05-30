from functools import wraps
from .request import Request
from .response import Response
import time


def logging_middleware(handler):
    @wraps(handler)
    def wrapper(request: Request):

        start = time.perf_counter()
        response: Response = handler(request)
        elapsed = time.perf_counter() - start
        print(
            f"{request.method} {request.path} -> {response.status} {(elapsed * 1000):.5f}ms"
        )

        return response

    return wrapper


def apply_middlewares(handler, middlewares):
    for mw in reversed(middlewares):
        handler = mw(handler)
    return handler

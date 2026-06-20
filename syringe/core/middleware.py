from functools import wraps
from .request.base import Request
from .response import Response
import time
from abc import ABC

class Middleware(ABC):
    pass
    
    
class LoggingMiddleware(Middleware):
    def __init__(self):
        super().__init__()

    def _verify(self, context):
        pass
        
    
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
        elapsed_ms = time.perf_counter() - start
        print(
            f"{request.method:<6} "
            f"{request._raw_path:<22} "
            f"-> {response.status:<3} "
            f"[{elapsed_ms:.4f} ms]"
        )

        return response

    return wrapper

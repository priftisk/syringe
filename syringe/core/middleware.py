from .response import Response
from syringe.core.context import RequestContext
from abc import abstractmethod


class Middleware:

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "run"):
            raise Exception(
                f"Middleware {cls.__name__} must implement run(self, context)"
            )

    @abstractmethod
    def run(self, context):
        pass


class AuthMiddleware(Middleware):
    def __init__(self):
        super().__init__()

    def run(self, context: RequestContext):
        pass
        # request = context.request
        # print(request.headers)


class LoggingMiddleware(Middleware):
    def __init__(self):
        super().__init__()

    def run(self, context: RequestContext):
        import time

        start = time.perf_counter()
        context.resolve()  # Logging needs the response.
        response: Response = context.response
        elapsed_ms = time.perf_counter() - start
        print(
            f"{context.request.method:<6} "
            f"{context.request._raw_path:<22} "
            f"-> {response.status:<3} "
            f"[{elapsed_ms:.4f} ms]"
        )

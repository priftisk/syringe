from syringe.core.response import Response
from syringe.core.request.base import Request


class View:

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._allowed_methods = [
            m.upper()
            for m in ["get", "post", "put", "patch", "delete"]
            if callable(getattr(cls, m, None))
        ]

    # Returns handler from view based on http request method
    def dispatch(self, request: Request) -> Response:
        handler: callable[Request] = getattr(self, request.method.lower(), None)
        if handler is None:
            return Response("Method Not Allowed", 405)
        return handler(request)

import inspect


class View:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._allowed_methods = [
            m.upper()
            for m in ["get", "post", "put", "delete"]
            if callable(getattr(cls, m, None))
        ]

    def dispatch(self, method, *args, **kwargs):
        handler = getattr(self, method.lower(), None)
        if handler is None:
            return f"405 Method Not Allowed", 405
        return handler(*args, **kwargs), 200


class ArticleView(View):
    def get(self):
        return "<h1>All articles</h1>"

    def post(self):
        return "<p>Article created</p>"

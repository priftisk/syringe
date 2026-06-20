from syringe.core.middleware import Middleware

class MiddlewareRegistry:
    _registry = []

def register_middlewares(mw_list: list[Middleware]):
    for mw in mw_list:
        if not issubclass(mw, Middleware):
            raise RuntimeError(f"Expected Middleware. Found: {mw.__name__}")
    MiddlewareRegistry._registry = mw_list


def apply_middlewares(context):
    for mw in reversed(MiddlewareRegistry._registry):
        mw().run(context)
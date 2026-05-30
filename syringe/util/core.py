def apply_middlewares(handler, middlewares):
    for mw in reversed(middlewares):
        handler = mw(handler)
    return handler

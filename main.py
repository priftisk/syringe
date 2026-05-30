import socket
from syringe.router import Router
from views import ArticleView, SearchView
from syringe.request import Request
from syringe.response import Response
from syringe.middleware import logging_middleware, apply_middlewares

router = Router()

router.route("/articles")(ArticleView)
router.route("/search")(SearchView)
middlewares = [logging_middleware]


def handle(raw: str) -> bytes:
    try:
        req = Request(raw)
    except (ValueError, IndexError):
        return bytes(Response("Bad Request", 500))

    handler = router.resolve(req)

    if handler is None:
        return bytes(Response("<h1>404 Not Found</h1>", 404))

    handler = apply_middlewares(handler=handler, middlewares=middlewares)

    response: Response = handler(req)

    return bytes(response)


def run(host="127.0.0.1", port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Serving on http://{host}:{port}")
    while True:
        conn, _ = server.accept()
        try:
            raw = conn.recv(4096).decode("utf-8")
            conn.sendall(handle(raw))
        finally:
            conn.close()


if __name__ == "__main__":
    run()

import socket
from syringe.router import Router
from views import ArticleView, SearchView
from syringe.util.response import make_response
from syringe.request import Request

router = Router()

router.route("/articles")(ArticleView)
router.route("/search")(SearchView)


def handle(raw: str) -> str:
    try:
        request = Request(raw)
    except ValueError:
        return make_response("Bad Request", 500)
    handler = router.resolve(request.method, request.path)
    if handler is None:
        return make_response("<h1>404 Not Found</h1>", 404)
    body, status = handler()
    return make_response(body, status)


def run(host="127.0.0.1", port=9999):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Serving on http://{host}:{port}")

    while True:
        conn, addr = server.accept()
        try:
            raw = conn.recv(4096).decode("utf-8")
            response = handle(raw)
            conn.sendall(response.encode("utf-8"))
        finally:
            conn.close()


if __name__ == "__main__":
    run()

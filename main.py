import socket
from router import Router

router = Router()


@router.route("/hello")
def hello():
    return "<h1>Hello, World!</h1>"


@router.route("/bye")
def bye():
    return "<h1>Goodbye!</h1>"


def make_response(body, status=200, content_type="text/html"):
    """Build a raw HTTP/1.1 response string."""
    status_text = {200: "OK", 404: "Not Found", 500: "Internal Server Error"}
    return (
        f"HTTP/1.1 {status} {status_text[status]}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        "\r\n" + body
    )


def handle(raw: str) -> str:
    """Parse the request, resolve a handler, return a response string."""
    try:
        first_line = raw.split("\r\n")[0]
        method, path, *_ = first_line.split()
    except ValueError:
        return make_response("Bad Request", 500)

    handler = router.resolve(method, path)

    if handler is None:
        return make_response("<h1>404 — Not Found</h1>", 404)

    body = handler()
    return make_response(body)


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

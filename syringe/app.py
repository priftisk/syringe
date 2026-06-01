from .router import Router
from .response import Response
from .request import Request
from .util.core import apply_middlewares
import socket


class SyringeApp:
    def __init__(self):
        self.router = Router()
        self.middlewares = []

    def route(self, path, **kwargs):
        return self.router.route(path, **kwargs)

    def use(self, mw):
        self.middlewares.append(mw)

    def __call__(self, request):
        handler = self.router.resolve(request)
        wrapped = apply_middlewares(handler, self.middlewares)
        return wrapped(request)

    def run(self, host="127.0.0.1", port=9999):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(5)
        print(f"Serving on http://{host}:{port} (Ctrl+C to stop)")

        try:
            while True:
                conn, _ = server.accept()
                try:
                    raw = conn.recv(4096).decode("utf-8")
                    conn.sendall(bytes(self(Request(raw))))  # invokes self.__call__
                finally:
                    conn.close()
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            server.close()

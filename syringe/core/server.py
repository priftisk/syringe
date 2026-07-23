from syringe.util.core import get_local_ip
from syringe.core.request.base import Request
from syringe.core.context import RequestContext, make_context
from syringe.registry.middleware import apply_middlewares

import socket

class SyringeServer:
    def __init__(self):
        self.host: str = get_local_ip()
        self.port: int = 9999
        self._max_conns: int = 12
        self._socket: socket.socket = None
        self._setup_socket()

    def run(self):
        self._socket.listen(self._max_conns)
        print(f"Serving on http://{self.host}:{self.port} (Ctrl+C to stop)")
        self._accept_conns()

    def _setup_socket(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind((self.host, self.port))
        except Exception as e:
            raise RuntimeError("Failed to setup server socket. ", e)

    def _handle_request(self, request: Request):
        context: RequestContext = make_context(request)
        apply_middlewares(context)
        if not context.resolved:
            context.resolve()
        return context.response

    def _serve_conn(self, conn: socket.socket):
        try:
            raw_data = conn.recv(4096).decode("utf-8")
            response = self._handle_request(Request(raw_data))
            conn.sendall(bytes(response))
        finally:
            conn.close()

    def _accept_conns(self):
        try:
            while True:
                conn, _ = self._socket.accept()
                self._serve_conn(conn)
        except KeyboardInterrupt:
            print("\nShutting down...")
        except Exception as e:
            print("ERROR:", repr(e))
        finally:
            self._socket.close()
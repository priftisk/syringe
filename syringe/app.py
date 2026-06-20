from syringe.core.context import make_context
from syringe.core.request.base import Request
from syringe.util.core import apply_middlewares, autodiscover
from syringe.util.core import get_local_ip
from syringe.core.context import RequestContext
import socket


class SyringeApp:
    def __init__(self, app_name=None):
        if not app_name:
            raise RuntimeError(
                "Create an app name. Make sure it matches the name of the root folder of your app. It will be used to discover declared routes."
            )
        self.app_name = app_name
        self.middlewares = []

    def use(self, mw_list):
        for mw in mw_list:
            self.middlewares.append(mw)

    def __call__(self, request: Request):
        context: RequestContext = make_context(request)
        # wrapped = apply_middlewares(context.target, self.middlewares)
        context.resolve()
        return context.response

   

    def run(self, host=None, port=9999):
        autodiscover(
            self.app_name
        )  # Discover and import View classes from folder named app_name
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host, port = host if host is not None else get_local_ip(), port
        server.bind((host, port))
        server.listen(5)
        print(f"Serving on http://{host}:{port} (Ctrl+C to stop)")

        try:
            while True:
                conn, _ = server.accept()
                try:
                    raw_data = conn.recv(4096).decode("utf-8")
                    conn.sendall(
                        bytes(self(Request(raw_data)))
                    )  # invokes self.__call__
                finally:
                    conn.close()
        except KeyboardInterrupt:
            print("\nShutting down...")
        except Exception as e:
            print("ERROR:", repr(e))

        finally:
            server.close()

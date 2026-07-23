from syringe.util.core import autodiscover
from syringe.core.server import SyringeServer
from syringe.core.router import route
from syringe.registry.middleware import register_middlewares

class SyringeApp:
    def __init__(self, app_name=None):
        if not app_name:
            raise RuntimeError(
                "Create an app name. Make sure it matches the name of the root folder of your app. It will be used to discover declared routes."
            )
        self.app_name = app_name
        self._server: SyringeServer = SyringeServer()

    def use(self, mw_list):
        register_middlewares(mw_list)
    
    def controller(self, path: str, methods=["GET"]):
        return route(path, methods)

    def run(self):
        autodiscover(
            self.app_name
        )  # Discover and import View classes from folder named app_name
        self._server.run()

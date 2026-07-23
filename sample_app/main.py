from syringe.app import SyringeApp
from syringe.core.middleware import LoggingMiddleware, AuthMiddleware

app = SyringeApp("sample_app")

app.use([LoggingMiddleware, AuthMiddleware])


if __name__ == "__main__":
    app.run()

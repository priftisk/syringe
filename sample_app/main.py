from syringe.app import SyringeApp
from syringe.core.middleware import LoggingMiddleware

app = SyringeApp("sample_app")

app.use([LoggingMiddleware])


if __name__ == "__main__":
    app.run()

from syringe.app import SyringeApp
from syringe.core.middleware import logging_middleware, not_found_middleware

app = SyringeApp("sample_app")

app.use(logging_middleware)
app.use(not_found_middleware)


if __name__ == "__main__":
    app.run()

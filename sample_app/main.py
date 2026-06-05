from syringe.app import SyringeApp
from syringe.core.middleware import logging_middleware, not_found_middleware
from sample_app.views import *

app = SyringeApp()

app.use(logging_middleware)
app.use(not_found_middleware)


if __name__ == "__main__":
    app.run()

from views import ArticleView, SearchView

# from syringe.response import Response
from syringe.app import SyringeApp
from syringe.middleware import logging_middleware, not_found_middleware

app = SyringeApp()

app.use(logging_middleware)
app.use(not_found_middleware)


# @app.route("/hello")
# def hello(req):
#     return Response("Hello")


app.router.route("/articles")(ArticleView)
app.router.route("/search")(SearchView)

if __name__ == "__main__":
    app.run()

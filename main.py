from views import ArticleView, SearchView
from syringe.app import SyringeApp
from syringe.middleware import logging_middleware, not_found_middleware
from syringe.response import Response

app = SyringeApp()

app.use(logging_middleware)
app.use(not_found_middleware)


@app.route("/hello")
def get_users(req):
    return Response("Hello")


app.route("/articles")(ArticleView)
app.route("/search")(SearchView)

if __name__ == "__main__":
    app.run()

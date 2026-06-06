from syringe.views.base import View
from syringe.core.response import Response
from syringe.core.request.base import Request
from syringe.core.router import route


@route(path="/search/:query/:page", methods=["POST"])
def index(req: Request):
    return Response(
        f"<h1>Results for {req.path.params.get("query")} on page {req.path.params.get("page")}</h1>"
    )


@route(path="/articles")
class ArticleView(View):
    def get(self, req: Request):
        return Response("<h1>All articles</h1>")

    def post(self, req: Request):
        return Response("Article created!")

    def patch(self, req: Request):
        return Response("Article patched!")

from syringe.views.base import View
from syringe.response import Response
from syringe.request import Request


class ArticleView(View):
    def get(self, req: Request):
        return Response("<h1>All articles</h1>")

    def post(self, req: Request):
        return Response("Article created!")

    def patch(self, req: Request):
        return Response("Article patched!")


class SearchView(View):
    def get(self, request: Request):

        return Response(
            f"Searching for {request.query_params.get("q")} on page {request.query_params.get("page")}"
        )

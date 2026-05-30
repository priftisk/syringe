from syringe.views import View
from syringe.response import Response


class ArticleView(View):
    def get(self, req):
        return Response("<h1>All articles</h1>")

    def post(self, req):
        return Response("Article created!")

    def patch(self, req):
        return Response("Article patched!")


class SearchView(View):
    def get(self, request):

        return Response(
            f"Searching for {request.query_params.get("q")} on page {request.query_params.get("page")}"
        )

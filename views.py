from syringe.views import View


class ArticleView(View):
    def get(self):
        return "<h1>All articles</h1>"

    def post(self):
        return "Article created!"

    def patch(self):
        return "Article patched!"


class SearchView(View):
    def get(self):

        return f"Searching"

# Syringe

A from-scratch implementation of a URL routing system inspired by Django and Flask class-based views. Built as a learning exercise in meta-Python — decorators, `inspect`, `Request`/`Response` objects, class-based view dispatch, and middleware chaining.

## Project structure

```
syringe/
├── syringe/            # core package
│   ├── app.py          # SyringeApp — the top-level application object
│   ├── middleware.py   # built-in middleware (logging, not_found)
│   ├── response.py     # Response class
│   ├── router.py       # Router — decorator factories, URL matching
│   └── views/
│       └── base.py     # View base class and dispatch logic
├── views.py            # example views (ArticleView, SearchView)
├── main.py             # entry point
├── Makefile            # `make run` → python main.py
└── reqs.http           # example HTTP requests
```

## What it covers

| Stage | Topic             | Concepts                                                      |
| ----- | ----------------- | ------------------------------------------------------------- |
| 1     | Basic router      | Decorator factories, dict-based dispatch                      |
| 2     | URL parameters    | Regex named capture groups, `re.fullmatch`                    |
| 3     | HTTP methods      | Method-keyed routes (`"GET /path"`), `resolve()`              |
| 4     | Class-based views | `inspect.isclass`, `View.dispatch`, per-request instantiation |
| 5     | Middleware        | Call stack chaining, `app.use()`                              |

## Running

```bash
make run
# or
python main.py
```

## Usage

### Creating an app

Routes and middleware are registered on a `SyringeApp` instance. Middleware runs in registration order; `app.run()` starts the server.

```python
from syringe.app import SyringeApp
from syringe.middleware import logging_middleware, not_found_middleware

app = SyringeApp()

app.use(logging_middleware)
app.use(not_found_middleware)
```

### Class-based views

Define views by subclassing `View` and implementing lowercase HTTP method handlers.

```python
from syringe.views.base import View
from syringe.response import Response

class ArticleView(View):
    def get(self, req):
        return Response("<h1>All articles</h1>")

    def post(self, req):
        return Response("Article created!")

    def patch(self, req):
        return Response("Article patched!")
```

### Registering routes

Pass view classes (or functions) to `app.route()`:

```python
from views import ArticleView, SearchView

app.route("/articles")(ArticleView)
app.route("/search")(SearchView)
```

The decorator-style alternative also works for function-based views:

```python
@app.route("/hello")
def hello(req):
    return Response("Hello")
```

### Query parameters

`request.query_params` exposes the parsed query string as a dict:

```python
class SearchView(View):
    def get(self, request):
        return Response(
            f"Searching for {request.query_params.get('q')} "
            f"on page {request.query_params.get('page')}"
        )
```

### Middleware

Middleware functions are registered with `app.use()` and form a call stack. Each middleware receives the request and a `next` callable:

```python
app.use(logging_middleware)
app.use(not_found_middleware)
```

`not_found_middleware` handles the case where no route matches — returning a 404 response so the caller doesn't need to check for `None`.

## Key implementation details

**`SyringeApp` facade** — the public API is `app.route()`, `app.use()`, and `app.run()`. Internally `SyringeApp` delegates URL matching to a `Router` and runs requests through the registered middleware stack before dispatching.

**Method-keyed routing** — routes are stored as `"METHOD /path"` strings (e.g. `"GET /articles"`), so method matching is an O(1) dict lookup. A view registered for multiple methods creates one entry per method pointing to the same handler.

**`resolve()` not `dispatch()`** — `resolve` returns a handler callable without calling it, separating routing from execution. The caller (or middleware) invokes the handler with the request, making it straightforward to add error handling around the call.

**Class-based view detection** — `resolve` uses `inspect.isclass` and `issubclass(target, View)` to distinguish view classes from plain functions. When a view class is matched, it wraps instantiation and `view.dispatch(request)` in a closure so the caller gets a uniform `handler(request)` interface regardless of how the route was registered.

**Per-request instantiation** — a fresh `View` instance is created on every request inside the handler closure, mirroring Django's behaviour and avoiding shared state between requests.
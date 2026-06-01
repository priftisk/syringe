# Flask-style URL router

A from-scratch implementation of a URL routing system inspired by Flask and Django's class-based views. Built as a learning exercise in meta-Python — decorators, `inspect`, `Request`/`Response` objects, and class-based view dispatch.

## What it covers

| Stage | Topic | Concepts |
|---|---|---|
| 1 | Basic router | Decorator factories, dict-based dispatch |
| 2 | URL parameters | Regex named capture groups, `re.fullmatch` |
| 3 | HTTP methods | Method-keyed routes (`"GET /path"`), `resolve()` |
| 4 | Class-based views | `inspect.isclass`, `View.dispatch`, per-request instantiation |
| 5 | Middleware | Call stack chaining |

## Usage

### Function-based routes

```python
from router import Router
from response import Response

router = Router()

@router.route('/')
def index(request):
    return Response("Hello!")

@router.route('/users', methods=['POST'])
def create_user(request):
    return Response("Created", status=201)

# Resolve returns a handler callable, then call it with the request
handler = router.resolve(request)
if handler:
    response = handler(request)
```

### Class-based views

```python
from views import View

@router.route('/users', methods=['GET', 'POST'])
class UserView(View):
    def get(self, request):
        return Response("List users")

    def post(self, request):
        return Response("Create user", status=201)

# resolve() detects the View subclass, instantiates it, and calls view.dispatch(request)
handler = router.resolve(request)
if handler:
    response = handler(request)
```

## Unmatched routes

`resolve()` returns `None` when no route matches — the caller decides how to handle it:

```python
handler = router.resolve(request)
if handler is None:
    response = Response("Not found", status=404)
else:
    response = handler(request)
```

## Key implementation details

**Method-keyed routing** — routes are stored as `"METHOD /path"` strings (e.g. `"GET /users"`), so method matching is O(1) dict lookup rather than a separate check. A view registered with `methods=['GET', 'POST']` creates two entries pointing to the same handler.

**`resolve()` not `dispatch()`** — `resolve` returns a handler callable without calling it, separating routing from execution. The caller invokes the handler with the request, which makes it straightforward to add middleware or error handling around the call.

**Class-based view detection** — `resolve` uses `inspect.isclass` and `issubclass(target, View)` to distinguish view classes from plain functions. When a view class is matched, it wraps instantiation and `view.dispatch(request)` in a closure so the caller gets a uniform `handler(request)` interface regardless of whether the route was registered as a function or a class.

**Per-request instantiation** — a fresh `View` instance is created on every request inside the handler closure, mirroring Django's behaviour and avoiding shared state between requests.
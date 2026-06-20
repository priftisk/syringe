import inspect
from typing import Callable
from syringe.views.base import View
from syringe.registry.router import get_route_handler

# A new RequestContext is created for every new request. 
class RequestContext:
    def __init__(self, request=None):
        if request is None:
            raise RuntimeError(
                "Cannot instantiate RequestContext without request argument."
            )

        self.request = request
        self.target = None
        self.response = None

        self._set_target(request)
    
    def _set_target(self, request):
        target = get_route_handler(request)
        if target is None:
            return
        if inspect.isclass(target) and issubclass(target, View):
            view = target()  # instantiate
            self.target = view.dispatch(context=self) # Pass context
            return
        if isinstance(target, Callable):
            self.target = target
            return

    def set_response(self, *args, **kwargs):
        pass


def make_context(request) -> RequestContext:
    context = RequestContext(request)
    return context

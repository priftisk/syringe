import inspect, types
from typing import Callable,Union
from syringe.views.base import View
from syringe.registry.router import get_route_handler
from syringe.core.response import Response
from syringe.core.request.base import Request

# A new RequestContext is created for every new request.
class RequestContext:
    def __init__(self, request=None):
        if request is None:
            raise RuntimeError(
                "Cannot instantiate RequestContext without request argument."
            )

        self.request: Request = request
        self.target: Union[Callable | View] = None # The handler defined by the user (func or View).
        self.response = None
        self.resolved: bool = False

        self._set_target(request)
    
        
   
    def _set_target(self, request):
        target = get_route_handler(request)

        if target is None or self.target is not None: # Prevent re-setting of self.target
            return

        if inspect.isclass(target) and issubclass(target, View):
            target = target().dispatch(context=self) # Asks the view for the specific handler based on request path

        elif not isinstance(target, types.FunctionType): # Not found
            return  #TODO Maybe dont fail silenty here

        self.target = target

    
    def resolve(self):
        if(self.resolved): return # resolve() called already
        self.resolved = True
        if not self.target: # Return 404 NOT FOUND
            self.response = Response(body=f"<h1>{self.request._raw_path}NOT FOUND</h1>", status=404)
            return
        self.response = self.target(self.request)
        


def make_context(request) -> RequestContext:
    context = RequestContext(request)
    return context

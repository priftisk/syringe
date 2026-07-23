from syringe.core.request.headers import Headers
from syringe.core.request.query_params import QueryParams
from syringe.core.request.path import RequestPath

class Request:
    headers = Headers() #lazy-loaded
    query_params = QueryParams() #lazy-loaded

    def __init__(self, raw: str):
        first_line = raw.split("\r\n")[0]
        self._raw = raw
        self.method, self._raw_path, *_ = first_line.split()
        self.path = RequestPath(self._raw_path)

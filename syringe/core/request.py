from syringe.util.descriptor.headers import Headers
from syringe.util.descriptor.query_params import QueryParams


class Request:
    headers = Headers()
    query_params = QueryParams()

    def __init__(self, raw: str):
        self._raw = raw
        first_line = raw.split("\r\n")[0]
        self.method, self._raw_path, *_ = first_line.split()
        self.path = self._raw_path.split("?")[0]  # clean path for routing

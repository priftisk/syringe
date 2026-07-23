from collections import defaultdict


class RequestPath:
    def __init__(self, raw_path):
        self.base = "/"
        self._params_list = []
        self.params = defaultdict(str)
        self._parse(raw_path)

    def _parse(self, raw_path):
        full = raw_path.split("?")[0]
        if full == "/":
            return

        path_parts = full.split("/")
        self.base = f"/{path_parts[1]}"

        self._params_list = path_parts[2::]

    def _set_params(self, route_params):
        for param, req_path_value in zip(
            sorted(route_params, key=lambda x: x.order), self._params_list
        ):
            self.params.setdefault(param.name, req_path_value)

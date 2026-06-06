class RouteParam:
    def __init__(self, name, order):
        self.name = name
        self.order = order

    def __getattr__(self, name):
        return self.__dict__.get(name, None)


class Route:
    def __init__(self, methods, raw_path):
        self.methods = methods
        self.base_path = None
        self.params = []
        self._parse(raw_path)

    def _parse(self, raw_path: str):
        if raw_path == "/":
            self.base_path = raw_path

        path_parts = raw_path.split("/")

        if len(path_parts) < 2:
            raise ValueError(f"Invalid path {raw_path} for route registration.")

        self.base_path = f"/{path_parts[1]}"

        order = 1
        for p in path_parts[1::]:
            if p.startswith(":"):
                self.params.append(RouteParam(p[1::], order))
                order += 1

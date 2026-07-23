from typing import List


class RouteParam:
    def __init__(self, name, order):
        self.name: str = name
        self.order: int = order

    def __getattr__(self, name):
        return self.__dict__.get(name, None)


class Route:
    def __init__(self, methods, raw_path):
        self.methods: List[str] = methods
        self.base_path: str = None
        self.params: List[RouteParam] = []
        self._parse(raw_path)

    def _parse_params(self, path_parts: List[str]):
        order = 1
        for p in path_parts[1::]:
            if p.startswith(":"):
                self.params.append(RouteParam(p[1::], order))
                order += 1

    def _parse(self, raw_path: str):
        if raw_path == "/":
            self.base_path = raw_path

        path_parts = raw_path.split("/")

        if len(path_parts) < 2:
            raise ValueError(f"Invalid path {raw_path} for route registration.")

        self.base_path = f"/{path_parts[1]}"

        self._parse_params(path_parts)
